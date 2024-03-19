from pydantic import BaseModel


class QueryResponse(BaseModel):
    """Simple model to hold the query and response."""

    prompt: str
    response: str

    # Allow Extra
    class Config:
        extra = "allow"


class UpdateResponse(BaseModel):
    """Simple model to hold the response to an update request."""

    message: str
    query: QueryResponse

    # Allow Extra
    class Config:
        extra = "allow"
