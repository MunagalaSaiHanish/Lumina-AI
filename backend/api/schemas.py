from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    source_type: str
    source: str


class AnalyzeResponse(BaseModel):
    success: bool
    message: str