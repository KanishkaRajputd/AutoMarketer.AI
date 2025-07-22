
import streamlit as st
import os

# Setup SQLite3 compatibility for Streamlit Cloud deployment
from utils.db_compatibility import setup_sqlite3_compatibility, get_chroma_settings
setup_sqlite3_compatibility()

# Try to import ChromaDB with fallback
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ ChromaDB import failed: {e}")
    CHROMADB_AVAILABLE = False
    # Import fallback implementation
    from utils.chromadb_fallback import get_safe_chroma_collection



def clear_chroma_db(collection_name=None):
    """
    Clear all documents from ChromaDB collection(s) with fallback support.
    
    Args:
        collection_name (str, optional): Name of specific collection to clear.
                                       If None, clears all collections.
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        persist_directory = "./chrome_store"
        
        # If ChromaDB is not available, use fallback clearing
        if not CHROMADB_AVAILABLE:
            print("📦 Using fallback ChromaDB clearing")
            try:
                if collection_name:
                    # Clear specific mock collection
                    session_key = f"chroma_mock_{collection_name}"
                    if session_key in st.session_state:
                        del st.session_state[session_key]
                        print(f"🗑️ Cleared mock collection '{collection_name}'")
                    
                    collections_key = "chroma_mock_collections"
                    if collections_key in st.session_state and collection_name in st.session_state[collections_key]:
                        del st.session_state[collections_key][collection_name]
                else:
                    # Clear all mock collections
                    collections_key = "chroma_mock_collections"
                    if collections_key in st.session_state:
                        collection_names = list(st.session_state[collections_key].keys())
                        for name in collection_names:
                            session_key = f"chroma_mock_{name}"
                            if session_key in st.session_state:
                                del st.session_state[session_key]
                        del st.session_state[collections_key]
                        print(f"🗑️ Cleared {len(collection_names)} mock collections")
                return True
            except Exception as e:
                print(f"Error clearing mock collections: {str(e)}")
                return False
        
        # Try to create the directory if it doesn't exist
        try:
            os.makedirs(persist_directory, exist_ok=True)
        except:
            pass
        
        # Use more compatible ChromaDB configuration
        try:
            # Try with optimized settings for cloud deployment
            settings = get_chroma_settings()
            chroma_client = chromadb.PersistentClient(
                path=persist_directory,
                settings=chromadb.config.Settings(**settings)
            )
        except Exception as e:
            print(f"Warning: Persistent storage failed, trying in-memory client: {e}")
            try:
                # Fallback to in-memory client with settings
                settings = get_chroma_settings()
                chroma_client = chromadb.Client(settings=chromadb.config.Settings(**settings))
            except Exception as e2:
                print(f"Warning: In-memory client with settings failed, using basic client: {e2}")
                # Last resort: basic client
                chroma_client = chromadb.Client()
        
        if collection_name:
            # Clear specific collection
            try:
                collection = chroma_client.get_collection(name=collection_name)
                all_items = collection.get()
                if all_items['ids']:
                    collection.delete(ids=all_items['ids'])
                    print(f"🗑️ Cleared ChromaDB collection '{collection_name}'")
                else:
                    print(f"📭 ChromaDB collection '{collection_name}' was already empty")
                return True
            except Exception as e:
                print(f"Collection '{collection_name}' not found or already cleared")
                return True
        else:
            # Clear all collections
            try:
                collections = chroma_client.list_collections()
                if collections:
                    for collection in collections:
                        chroma_client.delete_collection(name=collection.name)
                        print(f"🗑️ Deleted ChromaDB collection '{collection.name}'")
                else:
                    print("📭 No ChromaDB collections found")
                return True
            except Exception as e:
                print(f"Error clearing all collections: {str(e)}")
                return False
        
    except Exception as e:
        st.error(f"Error clearing ChromaDB: {str(e)}")
        return False


def get_chroma_collection(collection_name, persist_directory="./chrome_store"):
    """
    Get or create a ChromaDB collection with automatic fallback to mock implementation.
    
    Args:
        collection_name (str): Name of the collection
        persist_directory (str): Directory to persist ChromaDB data
        
    Returns:
        Collection or None: ChromaDB collection or mock collection
    """
    print(f"Collection name: {collection_name}")
    
    # If ChromaDB is not available, use fallback immediately
    if not CHROMADB_AVAILABLE:
        print("📦 Using fallback ChromaDB implementation")
        return get_safe_chroma_collection(collection_name, persist_directory)
    
    try:
        # Try to create the directory if it doesn't exist
        try:
            os.makedirs(persist_directory, exist_ok=True)
        except:
            pass
        
        # Use more compatible ChromaDB configuration
        try:
            # Try with optimized settings for cloud deployment
            settings = get_chroma_settings()
            chroma_client = chromadb.PersistentClient(
                path=persist_directory,
                settings=chromadb.config.Settings(**settings)
            )
        except Exception as e:
            print(f"Warning: Persistent storage failed, trying in-memory client: {e}")
            try:
                # Fallback to in-memory client with settings
                settings = get_chroma_settings()
                chroma_client = chromadb.Client(settings=chromadb.config.Settings(**settings))
            except Exception as e2:
                print(f"Warning: In-memory client with settings failed, using basic client: {e2}")
                # Last resort: basic client
                chroma_client = chromadb.Client()
        
        collection = chroma_client.get_or_create_collection(name=collection_name)
        return collection
        
    except Exception as e:
        st.error(f"Error accessing ChromaDB collection: {str(e)}")
        print("🔄 Falling back to mock ChromaDB implementation")
        return get_safe_chroma_collection(collection_name, persist_directory)