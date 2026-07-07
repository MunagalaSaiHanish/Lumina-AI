# Build structured context for the LLM


def build_context(documents):

    context_sections = []

    sources = []

    for document in documents:

        metadata = document["metadata"]

        source_type = metadata.get("source", "Unknown")

        title = ""

        if source_type == "youtube":

            title = metadata.get(
                "title",
                "YouTube Video"
            )

        elif source_type == "pdf":

            title = metadata.get(
                "file",
                "PDF Document"
            )

        elif source_type == "website":

            title = metadata.get(
                "url",
                "Website"
            )

        else:

            title = "Document"

        section = f"""
========================
SOURCE : {source_type.upper()}
TITLE  : {title}
========================

{document["text"]}
"""

        context_sections.append(section)

        if title not in sources:

            sources.append(title)

    return {

        "context": "\n\n".join(context_sections),

        "sources": sources

    }