from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Load text file
loader = TextLoader("example.txt")
documents = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# Create embedding model
embedding_model = OpenAIEmbeddings()  # or HuggingFaceEmbeddings()

# Create FAISS vector store
vectorstore = FAISS.from_documents(docs, embedding_model)

# Save locally
vectorstore.save_local("faiss_index")
