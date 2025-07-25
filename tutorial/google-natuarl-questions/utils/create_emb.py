from langchain_huggingface import HuggingFaceEmbeddings
import torch

def get_embedding_model(model_name: str):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device}
    )