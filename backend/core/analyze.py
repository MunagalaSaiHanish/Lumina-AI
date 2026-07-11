from api.schemas import AnalyzeRequest


class AnalyzeWorkflow:

    def run(self, request: AnalyzeRequest):

        source_type = request.source_type.lower()

        if source_type == "youtube":
            return {
                "success": True,
                "message": "YouTube analysis will be connected next."
            }

        elif source_type == "pdf":
            return {
                "success": True,
                "message": "PDF analysis will be connected next."
            }

        elif source_type == "website":
            return {
                "success": True,
                "message": "Website analysis will be connected next."
            }

        elif source_type == "text":
            return {
                "success": True,
                "message": "Text analysis will be connected next."
            }

        return {
            "success": False,
            "message": "Unsupported source type."
        }