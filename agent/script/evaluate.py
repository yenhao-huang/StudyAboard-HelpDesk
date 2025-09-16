import os
from dotenv import load_dotenv
load_dotenv()

import argparse
import pandas as pd
import time
from tqdm import tqdm
from typing import List, Tuple, Dict, Any
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

from rag_main import get_params
from utils.rag.build_rag import chat_without_rag, chat_with_rag, get_retriever
from params import PARAMS_ALIBABA, PARAMS_ALIBABA_WORAG, PARAMS_SENTENCE

def create_parser():
    parser = argparse.ArgumentParser(description="Evaluate retrieval results")
    parser.add_argument(
        "--query",
        type=str,
        default="美國那麼大？應該如何選擇學校呢？",
        help="question"
    )
    parser.add_argument(
        "--benchmark_dir",
        type=str,
        default="../data/eval/retrieval",
        help="Directory to the benchmark"
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="../results/retrieval/evaluation_results_test.csv",
        help="Path to save the evaluation results"
    )
    parser.add_argument(
        "--setting",
        type=str,
        default="alibaba",
        help="Retrieval setting name"
    )
    parser.add_argument(
        "--eval_type",
        type=str,
        default="generation",
        help="Type of evaluation to perform"
    )
    parser.add_argument(
        "--openrouter_setting",
        type=int,
        default=0,
        choices=[0, 1],
        help="OpenRouter setting: 0 for default, 1 for alternative"
    )
    return parser


def eval_retrie_unit(file_path: str, retriever: object, k: int) -> Tuple[List[Dict[str, Any]], int, int]:
    """
    回傳: (results, n_correct, n_total)
    results: 每題的檢索詳情（含是否正確與正確文件排名）
    n_correct: 命中的題數
    n_total: 題目總數
    """
    if not os.path.exists(file_path):
        print(f"[WARN] File not found, skipped: {file_path}")
        return [], 0, 0

    gt_data = pd.read_csv(file_path)
    n_correct = 0
    results: List[Dict[str, Any]] = []

    for _, row in gt_data.iterrows():
        query = row["question"]
        gt_source = row["uuid"]

        # 取前 k 筆
        docs = retriever.get_relevant_documents(query)[:k]
        retrieved_id = [doc.metadata.get("uuid") for doc in docs]

        # 是否命中 + 排名（1-based；未命中為 None）
        if gt_source in retrieved_id:
            rank = retrieved_id.index(gt_source) + 1
            n_correct += 1
            is_correct = True
        else:
            rank = None
            is_correct = False

        results.append({
            "question": query,
            "gt_uuid": gt_source,
            "retrieved_uuid": retrieved_id,
            "is_correct": is_correct,
            "rank": rank,         # ground-truth 在前 k 的名次（None 表示未命中）
            "k": k
        })

    return results, n_correct, len(gt_data)

def evaluate_retrieval(benchmark_dir: str, output_path: str, params: object):
    # 建立 retriever
    retriever = get_retriever(params.faiss_idx_path, params.emb_model, params.k)
    k = params.k

    # 要評估的檔案清單（可依需求增減）
    eval_files = [
        os.path.join(benchmark_dir, "faq.csv"),
        os.path.join(benchmark_dir, "faq_rephrased_full.csv"),
        os.path.join(benchmark_dir, "military_questions.csv"),
        os.path.join(benchmark_dir, "usrexp.csv"),
    ]

    all_rows: List[Dict[str, Any]] = []
    total_correct = 0
    total_count = 0

    for path in eval_files:
        rows, n_corr, n_tot = eval_retrie_unit(path, retriever, k)
        all_rows.extend(rows)
        total_correct += n_corr
        total_count += n_tot
        print(f"{os.path.basename(path)}: ({n_corr}/{n_tot})")

    if total_count == 0:
        print("[ERROR] No samples found. Nothing to evaluate.")
        return None

    precision_at_k = total_correct / total_count

    # 存結果
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(all_rows)
    df.to_csv(output_path, index=False)

    print("\n--- Summary ---")
    print(f"Total evaluated samples: {total_count}")
    print(f"Correctly retrieved count: {total_correct}")
    print(f"Precision@{k}: {precision_at_k:.4f}")

    return {
        "precision_at_k": precision_at_k,
        "k": k,
        "total": total_count,
        "correct": total_correct,
        "output_path": output_path,
    }


def get_llm_judger(chat_model: str, api_key: str) -> LLMChain:
    llm = ChatOpenAI(
        model=chat_model,
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0,
    )


    # without ground truth
    prompt = PromptTemplate.from_template(
        "請根據以下 Question 判斷模型的回答是否合理：\n\n"
        "Question:\n{question}\n\n"
        "Answer:\n{answer}\n\n"
        "請只回答：「正確」或「不正確」。"
    )

    return LLMChain(llm=llm, prompt=prompt)

# without ground truth
def evaluate_gener_unit(file_path: str, chain_generation: object, llm_judger: object) -> None:
    df = pd.read_csv(file_path)
    results = [] 
    for i, row in tqdm(df.iterrows(), total=len(df)):
        question = row["question"]

        answer = chain_generation.invoke(question)
        try:
            result = llm_judger.run(question=question, answer=answer)
        except Exception as e:
            result = f"Error: {str(e)}"


        print(f"[{i+1}] 問題: {question}")
        print(f"回答: {answer}")
        print(f"評估結果: {result}")
        print("=" * 50)

        results.append({
            "question": question,
            "answer": answer,
            "evaluation": result
        })

        if (i + 1) % 4 == 0:
            print("已完成 4 筆，休息 180 秒...")
            time.sleep(180)

    return results

def evaluate_generation(benchmark_dir: str, output_path: str, params: object):
    # 要評估的檔案清單
    '''
    eval_files = [
        os.path.join(benchmark_dir, "faq_test.csv"),
        #os.path.join(benchmark_dir, "military_questions_test.csv"),
    ]
    '''
    eval_files = [
        os.path.join(benchmark_dir, "faq.csv"),
        os.path.join(benchmark_dir, "military_questions.csv"),
    ]

    # 建立 generation pipeline
    if params.with_rag:
        chain_generation = chat_with_rag(params)
    else:
        chain_generation = chat_without_rag(params)

    # 建立 LLM-judger
    llm_judger = get_llm_judger(params.judge_model, params.openrouter_api_key)

    # 對每一個檔案，對每一個問題進行評估
    results_all = []
    for file in eval_files:
        results = evaluate_gener_unit(file, chain_generation, llm_judger)
        results_all.extend(results)
    
    # 儲存成 CSV
    result_df = pd.DataFrame(results_all)
    result_df.to_csv(output_path, index=False)
    print("結果已儲存")

def evaluate_retrieval_query(query: str, params: object):
    # 建立 retriever
    retriever = get_retriever(params.faiss_idx_path, params.emb_model, params.k)
    k = params.k

    docs = retriever.get_relevant_documents(query)[:k]
    retrieved_docs = [(doc.metadata.get("question"), doc.page_content) for doc in docs]
    print(retrieved_docs)


if __name__ == "__main__":
    args = create_parser().parse_args()

    params = get_params(args.setting)
    
    if args.eval_type == "retrieval":
        # 評估檢索
        print("=== 評估檢索結果 ===")
        evaluate_retrieval(args.benchmark_dir, args.output_path, params)
    elif args.eval_type == "generation":
        # 評估生成
        print("=== 評估生成結果 ===")
        evaluate_generation(args.benchmark_dir, args.output_path, params)
    elif args.eval_type == "retrieval_perquestion":
        evaluate_retrieval_query(args.query, params)
    else:
        raise ValueError(f"Unsupported evaluation type: {args.eval}")