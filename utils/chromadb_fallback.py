# ChromaDB fallback mechanism for Streamlit Cloud deployment
import streamlit as st
import json
import os
from typing import Dict, List, Any, Optional

class MockChromaCollection:
    """
    Mock ChromaDB collection that stores data in session state
    when ChromaDB is not available.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.session_key = f"chroma_mock_{name}"
        
        # Initialize session state for this collection if not exists
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                'ids': [],
                'documents': [],
                'embeddings': [],
                'metadatas': []
            }
    
    def add(self, ids: List[str], documents: List[str], embeddings: List[List[float]], metadatas: Optional[List[Dict]] = None):
        """Add documents to the mock collection"""
        try:
            collection_data = st.session_state[self.session_key]
            
            if metadatas is None:
                metadatas = [{}] * len(ids)
            
            for i, (doc_id, doc, embedding, metadata) in enumerate(zip(ids, documents, embeddings, metadatas)):
                # Remove existing id if it exists
                if doc_id in collection_data['ids']:
                    idx = collection_data['ids'].index(doc_id)
                    collection_data['ids'].pop(idx)
                    collection_data['documents'].pop(idx)
                    collection_data['embeddings'].pop(idx)
                    collection_data['metadatas'].pop(idx)
                
                # Add new document
                collection_data['ids'].append(doc_id)
                collection_data['documents'].append(doc)
                collection_data['embeddings'].append(embedding)
                collection_data['metadatas'].append(metadata)
            
            st.session_state[self.session_key] = collection_data
            print(f"📝 Added {len(ids)} documents to mock collection '{self.name}'")
            
        except Exception as e:
            st.error(f"Error adding to mock collection: {str(e)}")
    
    def query(self, query_embeddings: List[List[float]], n_results: int = 10) -> Dict[str, List]:
        """Query the mock collection using basic similarity"""
        try:
            collection_data = st.session_state[self.session_key]
            
            if not collection_data['embeddings']:
                return {'documents': [[]], 'distances': [[]], 'ids': [[]]}
            
            # Simple similarity calculation (dot product)
            query_embedding = query_embeddings[0]
            similarities = []
            
            for embedding in collection_data['embeddings']:
                # Calculate cosine similarity
                dot_product = sum(a * b for a, b in zip(query_embedding, embedding))
                magnitude_a = sum(a * a for a in query_embedding) ** 0.5
                magnitude_b = sum(b * b for b in embedding) ** 0.5
                
                if magnitude_a > 0 and magnitude_b > 0:
                    similarity = dot_product / (magnitude_a * magnitude_b)
                else:
                    similarity = 0
                
                similarities.append(similarity)
            
            # Get top n_results
            indexed_similarities = list(enumerate(similarities))
            indexed_similarities.sort(key=lambda x: x[1], reverse=True)
            top_indices = [idx for idx, _ in indexed_similarities[:n_results]]
            
            result_docs = [collection_data['documents'][i] for i in top_indices]
            result_ids = [collection_data['ids'][i] for i in top_indices]
            result_distances = [1 - similarities[i] for i in top_indices]  # Convert similarity to distance
            
            return {
                'documents': [result_docs],
                'ids': [result_ids],
                'distances': [result_distances]
            }
            
        except Exception as e:
            st.error(f"Error querying mock collection: {str(e)}")
            return {'documents': [[]], 'distances': [[]], 'ids': [[]]}
    
    def get(self) -> Dict[str, List]:
        """Get all documents from the collection"""
        try:
            collection_data = st.session_state[self.session_key]
            return collection_data
        except Exception as e:
            st.error(f"Error getting from mock collection: {str(e)}")
            return {'ids': [], 'documents': [], 'embeddings': [], 'metadatas': []}
    
    def delete(self, ids: List[str]):
        """Delete documents by IDs"""
        try:
            collection_data = st.session_state[self.session_key]
            
            for doc_id in ids:
                if doc_id in collection_data['ids']:
                    idx = collection_data['ids'].index(doc_id)
                    collection_data['ids'].pop(idx)
                    collection_data['documents'].pop(idx)
                    collection_data['embeddings'].pop(idx)
                    collection_data['metadatas'].pop(idx)
            
            st.session_state[self.session_key] = collection_data
            print(f"🗑️ Deleted {len(ids)} documents from mock collection '{self.name}'")
            
        except Exception as e:
            st.error(f"Error deleting from mock collection: {str(e)}")


class MockChromaClient:
    """
    Mock ChromaDB client that stores collections in session state
    """
    
    def __init__(self):
        self.collections_key = "chroma_mock_collections"
        if self.collections_key not in st.session_state:
            st.session_state[self.collections_key] = {}
    
    def get_or_create_collection(self, name: str) -> MockChromaCollection:
        """Get or create a mock collection"""
        collections = st.session_state[self.collections_key]
        
        if name not in collections:
            collections[name] = True  # Just mark as existing
            st.session_state[self.collections_key] = collections
            print(f"📁 Created mock collection '{name}'")
        
        return MockChromaCollection(name)
    
    def get_collection(self, name: str) -> MockChromaCollection:
        """Get an existing mock collection"""
        collections = st.session_state[self.collections_key]
        
        if name not in collections:
            raise ValueError(f"Collection '{name}' does not exist")
        
        return MockChromaCollection(name)
    
    def list_collections(self) -> List[str]:
        """List all mock collections"""
        collections = st.session_state[self.collections_key]
        return list(collections.keys())
    
    def delete_collection(self, name: str):
        """Delete a mock collection"""
        collections = st.session_state[self.collections_key]
        
        if name in collections:
            del collections[name]
            st.session_state[self.collections_key] = collections
            
            # Also clear the collection data
            session_key = f"chroma_mock_{name}"
            if session_key in st.session_state:
                del st.session_state[session_key]
            
            print(f"🗑️ Deleted mock collection '{name}'")


def get_chromadb_client():
    """
    Get ChromaDB client with multiple fallback levels:
    1. Try regular ChromaDB
    2. Try ChromaDB with optimized settings
    3. Fall back to mock implementation
    """
    try:
        # First try regular import and setup
        import chromadb
        from utils.db_compatibility import get_chroma_settings
        
        try:
            # Try with optimized settings
            settings = get_chroma_settings()
            client = chromadb.PersistentClient(
                path="./chrome_store",
                settings=chromadb.config.Settings(**settings)
            )
            print("✅ Using ChromaDB PersistentClient with optimized settings")
            return client, False  # False means not using mock
            
        except Exception as e:
            print(f"⚠️ PersistentClient failed, trying in-memory: {e}")
            try:
                settings = get_chroma_settings()
                client = chromadb.Client(settings=chromadb.config.Settings(**settings))
                print("✅ Using ChromaDB in-memory client with settings")
                return client, False
                
            except Exception as e2:
                print(f"⚠️ In-memory client failed, trying basic client: {e2}")
                client = chromadb.Client()
                print("✅ Using basic ChromaDB client")
                return client, False
                
    except Exception as e:
        print(f"❌ ChromaDB completely unavailable: {e}")
        print("🔄 Falling back to mock ChromaDB implementation")
        st.warning("⚠️ ChromaDB is not available. Using simplified in-memory storage. File uploads will work but data won't persist between sessions.")
        return MockChromaClient(), True  # True means using mock


def get_safe_chroma_collection(collection_name: str, persist_directory: str = "./chrome_store"):
    """
    Safely get a ChromaDB collection with automatic fallback to mock implementation
    """
    try:
        client, is_mock = get_chromadb_client()
        collection = client.get_or_create_collection(name=collection_name)
        
        if is_mock:
            print(f"📁 Using mock collection '{collection_name}'")
        else:
            print(f"📁 Using ChromaDB collection '{collection_name}'")
            
        return collection
        
    except Exception as e:
        st.error(f"Error creating collection: {str(e)}")
        print(f"❌ Collection creation failed, using mock fallback")
        # Last resort: return mock collection
        mock_client = MockChromaClient()
        return mock_client.get_or_create_collection(collection_name) 