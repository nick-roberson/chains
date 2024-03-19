# Standard Imports
import os
from rich import print

# Third Party Imports
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

# Local Imports
from backend.constants import PERSIST_DIR, TEXTS_DATA_PATH


############################################
# Index Singleton                          #
############################################

_INDEX = None


def get_index():
    """Get the index."""
    global _INDEX
    if _INDEX is None:
        _INDEX = load_data()
    return _INDEX


############################################
# API Key                                  #
############################################


def check_api_key():
    """Check the API Key."""
    API_KEY = os.environ.get("OPENAI_API_KEY")
    if API_KEY is None:
        raise ValueError("API Key not found")
    else:
        print("API Key found")


############################################
# Knowledge Base                           #
############################################


def load_data():
    """Load the data, returning the index."""
    # If the storage directory is empty, create the index
    if len(os.listdir(PERSIST_DIR)) == 0:
        return update_knowledge_base()
    # Otherwise, load the knowledge base
    else:
        return load_knowledge_base()


def load_knowledge_base():
    """Load the knowledge base."""
    # Load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    return index


def update_knowledge_base():
    """Update the knowledge base."""
    # If the data directory is empty or does not exist, raise an error
    if not os.path.exists(TEXTS_DATA_PATH) or len(os.listdir(TEXTS_DATA_PATH)) == 0:
        raise ValueError(f"Data directory {TEXTS_DATA_PATH} does not exist")

    # Clear out all data in the storage directory
    if os.path.exists(PERSIST_DIR):
        for file in os.listdir(PERSIST_DIR):
            os.remove(os.path.join(PERSIST_DIR, file))

    # Load the documents and create the index
    documents = SimpleDirectoryReader(TEXTS_DATA_PATH).load_data()
    print(f"Loaded {len(documents)} documents")

    # Create the index and return
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    return index


############################################
# Query Model w/ KB                        #
############################################


def submit_query(query: str) -> str:
    """Run the main function."""
    # Get the index if already loaded, otherwise load it
    index = get_index()
    # Run the query
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response
