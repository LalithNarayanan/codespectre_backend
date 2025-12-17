import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        "google": {
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "base_url": os.getenv("GOOGLE_BASE_URL"),
            "model": "gemini-2.5-flash-lite"
        },
        "openai": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL"),
            "model": "gpt-4o-mini"
        },
        "gemma3:12b": {
            "api_key": None,  # Ollama doesn't need real API key
            "base_url": "http://10.170.85.12:11434",  # Ollama with OpenAI compatibility
            "model": "gemma3:12b"  # or "gemma3:1b" for faster
        },
        "gemma12b": {
            "api_key": None,
            "base_url": "http://10.144.25.48:8087/",
            "model": "gemma12b",
            "endpoint": "/message/gemma12b"
        },
        "ollama": {
            "api_key": os.getenv("OLLAMA_API_KEY"),
            "base_url": os.getenv("OLLAMA_BASE_URL"),
            "model": "llama3.2"
        },
        "embeddings": {
            "emdbeddings_llama": "llama3.2",
            "embeddings_google": "models/embedding-001"
        },
        "sourcecode": {
            "source_code_path": "./source_code_to_process/Library-Management-System-JAVA-master",
            "source_code_ext": "**/*.java"
        },
        "vector": {
            "chroma_directory": "./chroma_db/sourcecode_lms",
            "chroma_collection_name": "sourcecode_lms"
        }
    }


# Available Models gemini : 
# gemini-2.0-flash
# gemini-2.5-flash
# gemini-2.5-pro
#gemini-2.0-flash-lite
#gemini-2.5-flash-lite     (fastest)