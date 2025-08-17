import os
import pandas as pd

IN_DIR = "../../data/docs/common_questions/"
TEMPLATE_PATH = "../../data/metadata/faq.csv"
OUTPUT_PATH = "../../data/eval/retrieval/faq.csv"
N_EVAL = 30


if __name__ == "__main__":
    df_all = []
    for file in os.listdir(IN_DIR):
        if file.endswith(".csv"):
            input_path = os.path.join(IN_DIR, file)
            df = pd.read_csv(input_path)
            df_all.append(df)
        
    df_all = pd.concat(df_all, ignore_index=True)
    cols = [c for c in df_all.columns if c not in ["answer", "source"]]
    df_all = df_all[cols + ["answer", "source"]]
    df_all.to_csv(TEMPLATE_PATH, index=False)
    print(df_all)

    if len(df_all) > N_EVAL:
        df_sample = df_all.sample(n=N_EVAL, random_state=42)
    else:
        raise ValueError(f"Data {len(df_all)} < asked files {N_EVAL}")

    df_sample.to_csv(OUTPUT_PATH, index=False)
    print(f"Sampled {len(df_sample)} rows to {OUTPUT_PATH}")
    print("Done!")