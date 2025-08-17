import unicodedata
import pandas as pd

def normalize_str(s: str) -> str:
    # 全形轉半形，去空白，轉小寫
    return unicodedata.normalize("NFKC", s).strip().lower()


def count_correct_answers(input_file: str) -> None:
    # 讀取評估結果檔案
    answer_df = pd.read_csv(input_file)

    n_corr, n_incorr = 0, 0
    for i, row in answer_df.iterrows():
        ans = normalize_str(row["evaluation"])
        if ans == "正確":
            n_corr += 1
        elif ans == "不正確":
            n_incorr += 1
        else:
            print(f"未知答案: {repr(ans)}")

    print(f"答對比例: {n_corr/(n_corr+n_incorr)} ({n_corr}/{n_corr+n_incorr})")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="計算正確答案數量")
    parser.add_argument("--input_file", type=str, required=True, help="評估結果檔案路徑 (e.g., evaluation_results.csv)")
    args = parser.parse_args()

    qa_eval_dir = "../../results/qa/"
    input_file = qa_eval_dir + args.input_file
    count_correct_answers(input_file)