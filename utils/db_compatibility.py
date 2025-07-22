# SQLite3 compatibility for Streamlit Cloud
import sys
import os

def setup_sqlite3_compatibility():
    """
    Set up SQLite3 compatibility for ChromaDB on Streamlit Cloud.
    This replaces the default sqlite3 module with pysqlite3-binary when available.
    """
    try:
        # Check if we're in a Streamlit Cloud environment
        is_streamlit_cloud = (
            os.environ.get('STREAMLIT_CLOUD', False) or
            os.environ.get('STREAMLIT_SERVER_PORT', False) or
            'streamlit' in os.environ.get('PATH', '')
        )
        
        if is_streamlit_cloud:
            print("🌐 Detected Streamlit Cloud environment")
            
        # Try to import pysqlite3-binary and replace sqlite3
        import pysqlite3
        sys.modules['sqlite3'] = pysqlite3
        sys.modules['sqlite3.dbapi2'] = pysqlite3
        print("✅ Using pysqlite3-binary for SQLite3 compatibility")
        
        # Additional environment setup for ChromaDB
        os.environ['SQLITE_THREADSAFE'] = '1'
        
    except ImportError as e:
        print(f"⚠️ pysqlite3-binary not available: {e}")
        print("ℹ️ Using system sqlite3 - may cause issues in cloud deployment")
    except Exception as e:
        print(f"❌ Error setting up SQLite3 compatibility: {e}")
        
def get_chroma_settings():
    """
    Get ChromaDB settings optimized for Streamlit Cloud deployment.
    """
    return {
        'allow_reset': True,
        'anonymized_telemetry': False,
    } 