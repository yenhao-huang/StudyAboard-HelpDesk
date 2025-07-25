import json
import os

from datasets import DatasetDict, Dataset, load_dataset
from transformers import AutoTokenizer
from sklearn.model_selection import train_test_split

def prompt_engineer(
    context,
    query,
    tokenizer, 
):
    prompt = f"""Context:
    {context}

    Question:
    {query}

    Answer:
    """
    messages = [
        {"role": "user", "content": prompt}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True # Switches between thinking and non-thinking modes. Default is True.
    )

    return text

def data_preprocess(
    context, 
    query,
    model_name,
    sequence_len=16384
):
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    raw_data = prompt_engineer(context, query, tokenizer)

    tokenized_data = tokenizer(
        raw_data,
        return_tensors="pt",
        truncation=True,
        max_length=sequence_len
    )

    return tokenized_data, tokenizer