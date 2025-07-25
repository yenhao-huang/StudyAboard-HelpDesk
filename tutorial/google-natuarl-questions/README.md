# Tutorial: Google Natural Questions

## How to run

Run the following scripts in order and run in workspace:

```bash
python script/prep_data.py              # Prepare Google Natural Questions (100K)
python script/build_faiss_idx.py       # Build FAISS index from passage embeddings
python script/retrieval_generation.py  # Run the retrieval-augmented generation pipeline
```

### Question/Answer Example

```text
Question: "Who produces the most wool in the world?"
Answer: China is currently the largest producer of wool by volume, followed by Australia.

Question: "Who discovered gravity?"
Answer: Sir Isaac Newton is credited with discovering the concept of gravity in the late 17th century.

Question: "What is the population of Canada?"
Answer: As of 2024, the population of Canada is approximately 40 million people.

Question: "When was the Eiffel Tower built?"
Answer: The Eiffel Tower was completed in 1889 for the Exposition Universelle (World’s Fair) held in Paris.
```

### Scripts/

- Retreived Document related
    - `append_file.py` : update index when adding new file
    - `prep_data.py`: download Google Natual Questions
    - `build_faiss_idx.py` : translate it into embedding and continue converting it into faiss index
- Chatbot-related
    - `search_faiss_idx.py` : find top-k related document
    - `custom_chatbot.py`: chatbot can be used to finetune
    - `openrouter_chatbot.py`: chatbot from openrouter
    - `retreival_generation`: connect between retreival and LLM chabot

## Components

### Datasets

- Natural Questions
    - Questions: Google, real google search queries
    - Answer: Full Wikipedia
    - Download framework: Huggingface Dataset
- Format (`.json`)

```jsx
{
	"query": ["query1", ...],
	"answer": ["answer1"],
}
```

### Embedding Model

- sentence-transformers/all-MiniLM-L6-v2
    - 22M
- Qwen/Qwen3-Embedding-8B
    - MTEB Leaderboard
        - Benchmark
        - Tasks
            - classification (e.g., finance news, millitary news)
            - retrieval
            - summarization

### Model

Input: context, user query
Model: deepseek-r1-8B
Output: LLM answer