from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# Load vectorstore
vectorstore = FAISS.load_local("faiss_index", embedding_model)

# Create retriever + LLM
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(model="gpt-3.5-turbo")  # or GPT-4 if you prefer

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Ask a question
query = "What is the document about?"
response = qa_chain.run(query)
print(response)
