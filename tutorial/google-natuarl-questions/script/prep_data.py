from datasets import load_dataset
import json
import os

if __name__ == "__main__":
    # load the first 1000 data
    dataset = load_dataset("sentence-transformers/natural-questions", split="train")

    # Save to json
    os.makedirs("data", exist_ok=True)
    with open("data/nq_passages.json", "w", encoding="utf-8") as f:
        json.dump(dataset[:], f, indent=2, ensure_ascii=False)

    print(f"Saved {len(dataset)} entries to nq_passages.json")

    dataset = load_dataset("sentence-transformers/natural-questions", split="train[:1000]")
    
    # Save to json
    os.makedirs("data", exist_ok=True)
    with open("data/nq_passages_1000.json", "w", encoding="utf-8") as f:
        json.dump(dataset[:], f, indent=2, ensure_ascii=False)

    print(f"Saved {len(dataset)} entries to nq_passages.json")
