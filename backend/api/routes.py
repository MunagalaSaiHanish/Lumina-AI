from fastapi import APIRouter

from api.schemas import AnalyzeRequest
from core.analyze import AnalyzeWorkflow

router = APIRouter()

workflow = AnalyzeWorkflow()


@router.get("/ping")
def ping():
    return {
        "message": "Lumixa API is running."
    }


@router.post("/analyze")
def analyze(request: AnalyzeRequest):

    return workflow.run(request)