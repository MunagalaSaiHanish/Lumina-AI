# ---------------------------------------------------------
# Build Context for LLM
# ---------------------------------------------------------

def build_context(documents):

    context_parts = []

    sources = []

    for document in documents:

        # -------------------------------
        # Context sent to the LLM
        # -------------------------------

        context_parts.append(
            document["text"]
        )

        # -------------------------------
        # Build Source Information
        # -------------------------------

        metadata = document.get(
            "metadata",
            {}
        )

        source_type = metadata.get(
            "source",
            "unknown"
        )

        # -------------------------------
        # YouTube
        # -------------------------------

        if source_type == "youtube":

            source = f"🎥 {metadata.get('title','YouTube')}"

            if metadata.get("channel"):

                source += f" • {metadata['channel']}"

        # -------------------------------
        # PDF
        # -------------------------------

        elif source_type == "pdf":

            source = f"📄 {metadata.get('file','PDF')}"

            if metadata.get("page"):

                source += f" • Page {metadata['page']}"

        # -------------------------------
        # Website
        # -------------------------------

        elif source_type == "website":

            source = f"🌐 {metadata.get('title','Website')}"

        # -------------------------------
        # Notes
        # -------------------------------

        elif source_type == "text":

            source = "📝 User Notes"

        else:

            source = "Unknown Source"

        # Avoid duplicate sources

        if source not in sources:

            sources.append(
                source
            )

    return {

        "context": "\n\n".join(
            context_parts
        ),

        "sources": sources

    }