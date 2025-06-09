import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Initialize ChromaDB client   
client = chromadb.HttpClient(
    host="localhost",
    port=8000,
    settings=Settings(allow_reset=True)
)

#natural language model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create or get a collection
collection = client.get_or_create_collection(
    name="natural_language_embeddings",
    metadata={"description": "Natural language text embeddings"}
)

# Sample texts to embed and store
texts = [
    "This is a sample document about machine learning.",
    "ChromaDB is a vector database for AI applications.",
    "Natural language processing helps computers understand text.",
    "Embeddings capture semantic meaning in numerical form."
]

embeddings = model.encode(texts).tolist()

# Store in ChromaDB
collection.add(
    embeddings=embeddings,
    documents=texts,
    ids=[f"doc_{i}" for i in range(len(texts))]
)

print(f"Added {len(texts)} documents to ChromaDB")
print(f"Collection count: {collection.count()}")

# Test a query
query_text = "What is machine learning?"
query_embedding = model.encode([query_text]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

print("\nQuery results:")
for i, doc in enumerate(results['documents'][0]):
    print(f"{i+1}. {doc}")



# Load CodeBERT model and tokenizer
#tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
#model = AutoModel.from_pretrained("microsoft/codebert-base")

# Encode a code snippet
#code_snippet = "def greet(name): return f'Hello {name}'"
#inputs = tokenizer(code_snippet, return_tensors="pt")

# Get the embeddings
#with torch.no_grad():
#    outputs = model(**inputs)

# Use the [CLS] token embedding or mean pooling
#embedding = outputs.last_hidden_state.mean(dim=1).squeeze()

#print(embedding.shape)  # torch.Size([768])