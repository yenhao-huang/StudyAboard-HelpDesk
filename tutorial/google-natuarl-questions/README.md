# Tutorial: Google Natural Questions

## How to run

Run the following scripts in order:

```bash
python script/prep_data.py              # Prepare and clean the raw dataset
python script/build_faiss_idx.py       # Build FAISS index from passage embeddings
python script/retrieval_generation.py  # Run the retrieval-augmented generation pipeline
```

### Example

```text
Question: Who produces the most wool in the world?
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

Output: LLM answer

## Checklist

### Prepare Libaraires & Dataset

- [x]  Install required libraries: `datasets`, `sentence-transformers`, `faiss-cpu`, `openai`
- [x]  Load the **Natural Questions** dataset (`train[:100]` for sampling)
- [x]  Save the cleaned passages to a local file (e.g., `nq_passages.json`)

---

### Embedding & Indexing

- [x]  Load passages from `nq_passages.json`
- [x]  Initialize the embedding model (e.g., `all-MiniLM-L6-v2`)
- [x]  Encode all passages into dense vectors
- [x]  Build a FAISS index (`IndexFlatL2`)
- [x]  Save the FAISS index as `nq_index.faiss`
- [x]  Create append file function

---

### Retriever

- [x]  Take user input as a query
- [x]  Use FAISS to search for top-k similar passages
- [x]  Collect the retrieved passages and print for inspection

---

### Generator

- [x]  Concatenate the retrieved passages into a prompt
- [x]  Format the prompt with structure:
    
    ```
    Context:
    [retrieved_passages]
    
    Question:
    [user_query]
    
    Answer:
    
    ```
    
- [x]  Call LLM (e.g., `Qwen-3`) with the prompt
- [x]  Print or display the generated answer

---

### Testing

- [ ]  Try multiple real-world queries like:
    - "Who discovered gravity?"
    - "What is the population of Canada?"
    - "When was the Eiffel Tower built?"
- [ ]  Check if the generated answers match the retrieved context
- [ ]  Evaluate quality of both retrieval and generation
- [ ]  Optionally log answers and context for review

---