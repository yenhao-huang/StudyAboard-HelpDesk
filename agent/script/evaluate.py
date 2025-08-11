import os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import time
from tqdm import tqdm
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

from rag_main import chat_with_rag, get_retriever
from params import PARAMS

def get_correctness_chain():
    llm = ChatOpenAI(
        model="moonshotai/kimi-k2:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0,
    )

    prompt = PromptTemplate.from_template(
        "請根據以下 Ground Truth 判斷模型的回答是否正確：\n\n"
        "Ground Truth:\n{ground_truth}\n\n"
        "Answer:\n{answer}\n\n"
        "請只回答：「正確」或「不正確」。"
    )

    return LLMChain(llm=llm, prompt=prompt)

def evaluate_retrieval(input_path: str):
    retriever = get_retriever(PARAMS.faiss_idx_path, PARAMS.emb_model, PARAMS.k)
    
    # Load ground truth data
    gt_data = pd.read_csv(input_path)

    top_k = PARAMS.k
    correct_count = 0
    results = []  # 儲存每筆資料的評估結果

    for i, row in gt_data.iterrows():
        query = row["question"]
        gt_source = row["answer"]
        print(query)
        # Perform retrieval
        docs: list[Document] = retriever.get_relevant_documents(query)
        print(docs)
        # Check if any of top-k has correct source
        retrieved_id = [doc.metadata["chunk_id"] for doc in docs]

        # 判斷是否正確
        is_correct = False
        if gt_source in retrieved_id:
            correct_count += 1
            is_correct = True
        
        # 儲存結果
        results.append({
            "question": query,
            "gt_source": gt_source,
            "retrieved_sources": retrieved_sources,
            "is_correct": is_correct
        })

    # 計算 Precision@k
    precision_at_k = correct_count / len(gt_data)

    # 將結果轉換為 DataFrame
    results_df = pd.DataFrame(results)

    # 印出所有結果
    print("--- Individual Retrieval Results ---")
    print(results_df)

    # 可以選擇將結果儲存到 CSV 檔案
    results_df.to_csv("../results/retrieval_evaluation_results.csv", index=False)

    print("\n--- Summary ---")
    print(f"Total evaluated samples: {len(gt_data)}")
    print(f"Correctly retrieved count: {correct_count}")
    print(f"Precision@{top_k}: {precision_at_k:.4f}")


def evaluate_generation():
    # 載入 CSV（假設已放置在同目錄下）
    df = pd.read_csv("../data/test/IDP_QA_Dataset.csv")

    # 初始化鏈
    correctness_chain = get_correctness_chain()
    chain_rag = chat_with_rag(PARAMS.emb_model, PARAMS.faiss_idx_path, PARAMS.k, PARAMS.chatbot_model)

    results = [] 
    for i, row in tqdm(df.iterrows(), total=len(df)):
        question = row["question"]
        ground_truth = row["ground_truth"]

        answer = chain_rag.invoke(question)

        try:
            result = correctness_chain.run(ground_truth=ground_truth, answer=answer)
        except Exception as e:
            result = f"Error: {str(e)}"

        print(f"[{i+1}] 問題: {question}")
        print(f"回答: {answer}")
        print(f"評估結果: {result}")
        print("=" * 50)

        results.append({
            "question": question,
            "answer": answer,
            "ground_truth": ground_truth,
            "evaluation": result
        })

        if (i + 1) % 4 == 0:
            print("已完成 8 筆，休息 90 秒...")
            time.sleep(180)

    # 儲存成 CSV
    result_df = pd.DataFrame(results)
    result_df.to_csv("qa_eval_result.csv", index=False)
    print("結果已儲存至 qa_eval_result.csv")

if __name__ == "__main__":
    input_path = "../data/eval/retrieval/common_questions.csv"
    evaluate_retrieval(input_path)