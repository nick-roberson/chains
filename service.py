# Standard Library
import argparse
import logging
import os
from typing import Dict

import uvicorn

# Third Party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rich import print

from backend.constants import (
    HOST_NAME,
    HOST_PORT,
    OPENAI_API_KEY,
    OPENAI_API_KEY_VAR,
    PERSIST_DIR,
    TEXTS_DATA_PATH,
)
from backend.llama import submit_query, update_knowledge_base

# Local
from models import QueryResponse, UpdateResponse

# Initialize FastAPI app and allow CORS
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Initialize manager and logger
logger = logging.getLogger(__name__)


@app.get("/")
def read_root() -> Dict:
    """Root endpoint."""
    return {"message": "Welcome to the Chain Texts Service"}


@app.get("/health")
def health() -> Dict:
    """Health endpoint."""
    return {"status": "UP"}


@app.post("/query")
def query(prompt: str) -> QueryResponse:
    """Query the index."""
    # Submit the query to the model
    result = submit_query(prompt)
    # Return query response
    return QueryResponse(
        prompt=prompt,
        response=result.response,
    )


@app.post("/reload")
def reload(test_prompt: str = None) -> UpdateResponse:
    """Reload the index."""
    # Clear and update the index based on any new data in the knowledge base
    update_knowledge_base()

    # If a test prompt is incuded, submit the prompt to the model
    if test_prompt:
        result = submit_query(test_prompt)
        return UpdateResponse(
            message="Index reloaded",
            query=QueryResponse(
                prompt=test_prompt,
                response=result.response,
            ),
        )
    else:
        return UpdateResponse(
            message="Index reloaded",
            query=None,
        )


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the FastAPI service")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Set logging level to DEBUG",
    )
    return parser.parse_args()


def configure_logging(level: int = logging.INFO):
    level = logging.DEBUG if os.environ.get("LOG_VERBOSE") is None else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def validate_startup():
    """Validate the startup environment"""
    # On startup check if the index path exists, if not create it
    if not os.path.exists(PERSIST_DIR):
        os.makedirs(PERSIST_DIR, exist_ok=True)

    # On startup check if the data path exists, if not raise an error, but create root of the path
    if not os.path.exists(TEXTS_DATA_PATH) or len(os.listdir(TEXTS_DATA_PATH)) == 0:
        os.makedirs(TEXTS_DATA_PATH, exist_ok=True)
        raise ValueError(
            f"Data directory {TEXTS_DATA_PATH} is empty, please add documents to the directory"
        )

    # Validate that the API Key is present
    if OPENAI_API_KEY is None:
        raise ValueError(
            f"API Key not found, please set the environment variable {OPENAI_API_KEY_VAR}"
        )


def run_service():
    """Run the FastAPI service."""
    args = parse_args()

    # Init logging
    configure_logging(level=logging.DEBUG if args.verbose else logging.INFO)

    # Log the startup vars
    print(
        f"""Starting up Chain Texts Service with the following configuration:
    - VERBOASE:         {args.verbose}
    - PERSIST_DIR:      {PERSIST_DIR}
    - TEXTS_DATA_PATH:  {TEXTS_DATA_PATH}
    """
    )

    # Run the app
    uvicorn.run(app, host=HOST_NAME, port=HOST_PORT)


if __name__ == "__main__":
    """Run the FastAPI service.

    Run:
        > poetry run uvicorn service:app --reload
    """
    # Validate the startup environment
    validate_startup()
    # Run the service
    run_service()
