import chromadb
from chromadb.config import Settings
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch
from typing import List, Dict, Any, Optional
import argparse

class RAGQuery:
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.HttpClient(
            host='localhost',
            port=8000,
            settings=Settings(allow_reset=True)
        )
        
        # Get collections
        self.nl_collection = self.client.get_collection('natural_language_embeddings')
        self.code_collection = self.client.get_collection('code_embeddings')
        
        # Initialize models
        self.nl_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.code_tokenizer = AutoTokenizer.from_pretrained('microsoft/codebert-base')
        self.code_model = AutoModel.from_pretrained('microsoft/codebert-base')
    
    def get_embedding(self, query: str, is_code: bool = False) -> List[float]:
        """Get embedding for a query using appropriate model"""
        if is_code:
            # Use CodeBERT for code queries
            inputs = self.code_tokenizer(query, return_tensors='pt', truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.code_model(**inputs)
            return outputs.last_hidden_state.mean(dim=1).squeeze().numpy().tolist()
        else:
            # Use sentence transformer for natural language queries
            return self.nl_model.encode([query])[0].tolist()
    
    def query(self, 
             query: str, 
             n_results: int = 3, 
             search_code: bool = True,
             search_nl: bool = True,
             where: Optional[Dict] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Query both collections and return combined results
        
        Args:
            query: The search query
            n_results: Number of results to return per collection
            search_code: Whether to search code collection
            search_nl: Whether to search natural language collection
            where: Optional metadata filter (e.g., {'file_type': 'code'})
        """
        results = {'code': [], 'nl': []}
        
        if search_code:
            try:
                code_embedding = self.get_embedding(query, is_code=True)
                code_results = self.code_collection.query(
                    query_embeddings=[code_embedding],
                    n_results=n_results,
                    where=where
                )
                
                # Format code results
                for i in range(len(code_results['documents'][0])):
                    results['code'].append({
                        'content': code_results['documents'][0][i],
                        'metadata': code_results['metadatas'][0][i],
                        'distance': code_results['distances'][0][i] if 'distances' in code_results else None
                    })
            except Exception as e:
                print(f"Error querying code collection: {e}")
        
        if search_nl:
            try:
                nl_embedding = self.get_embedding(query, is_code=False)
                nl_results = self.nl_collection.query(
                    query_embeddings=[nl_embedding],
                    n_results=n_results,
                    where=where
                )
                
                # Format NL results
                for i in range(len(nl_results['documents'][0])):
                    results['nl'].append({
                        'content': nl_results['documents'][0][i],
                        'metadata': nl_results['metadatas'][0][i],
                        'distance': nl_results['distances'][0][i] if 'distances' in nl_results else None
                    })
            except Exception as e:
                print(f"Error querying NL collection: {e}")
        
        return results

def print_results(results: Dict[str, List[Dict[str, Any]]]):
    """Pretty print the search results"""
    if results['code']:
        print('\n=== Code Results ===')
        for i, result in enumerate(results['code'], 1):
            try:
                metadata = result.get('metadata', {})
                print(f'\n{i}. From: {metadata.get("file_name", "Unknown file")}')
                print(f'   Type: {metadata.get("chunk_type", "Unknown type")}')
                if result.get('distance') is not None:
                    print(f'   Relevance: {1 - result["distance"]:.2%}')
                print(f'   Content: {result.get("content", "")[:200]}...')
            except Exception as e:
                print(f'\n{i}. Error displaying result: {e}')
    
    if results['nl']:
        print('\n=== Natural Language Results ===')
        for i, result in enumerate(results['nl'], 1):
            try:
                metadata = result.get('metadata', {})
                print(f'\n{i}. From: {metadata.get("file_name", "Unknown file")}')
                print(f'   Type: {metadata.get("chunk_type", "Unknown type")}')
                if result.get('distance') is not None:
                    print(f'   Relevance: {1 - result["distance"]:.2%}')
                print(f'   Content: {result.get("content", "")[:200]}...')
            except Exception as e:
                print(f'\n{i}. Error displaying result: {e}')

def clear_collections(self):
    """Clear all collections in ChromaDB"""
    try:
        # Reset the collections
        self.nl_collection.reset()
        self.code_collection.reset()
        print("Successfully cleared all collections")
    except Exception as e:
        print(f"Error clearing collections: {e}")

def main():
    parser = argparse.ArgumentParser(description='Query the RAG system')
    parser.add_argument('query', help='The search query')
    parser.add_argument('--n', type=int, default=3, help='Number of results per collection')
    parser.add_argument('--code-only', action='store_true', help='Search only code collection')
    parser.add_argument('--nl-only', action='store_true', help='Search only natural language collection')
    parser.add_argument('--file-type', help='Filter by file type (code/text)')
    parser.add_argument('--clear', action='store_true', help='Clear all collections')
    args = parser.parse_args()

    client = chromadb.HttpClient(
            host='localhost',
            port=8000,
            settings=Settings(allow_reset=True)
        )


    if args.clear:  # Add this argument
        nl_collection = client.get_collection(name="natural_language_embeddings")
        ml_collection = client.get_collection(name="code_embeddings")
        all_nl_items = nl_collection.get()
        all_ml_items = nl_collection.get()
        all_nl_ids = all_nl_items['ids']
        all_ml_ids = all_ml_items['ids']
        # Delete all documents in the collection
        nl_collection.delete(ids=all_nl_ids)  # this deletes everything
        ml_collection.delete(ids=all_ml_ids)
        return
    
    # Set up search parameters
    search_code = not args.nl_only
    search_nl = not args.code_only
    where = {'file_type': args.file_type} if args.file_type else None
    
    # Initialize and run query
    rag = RAGQuery()
    results = rag.query(
        query=args.query,
        n_results=args.n,
        search_code=search_code,
        search_nl=search_nl,
        where=where
    )
    
    print_results(results)

if __name__ == '__main__':
    main()


"""
basic examples: 

# Basic search
python query.py "how does the chunker work?"

# Search only code
python query.py "function that processes files" --code-only

# Search only documentation
python query.py "explain the embedding process" --nl-only

# Get more results
python query.py "your query" --n 5

# Filter by file type
python query.py "your query" --file-type code

"""