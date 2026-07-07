from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------
# Embedding Model
# ---------------------------------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ---------------------------------------------------------
# Generate Embeddings
# ---------------------------------------------------------

def generate_embeddings(chunks):

    if not chunks:

        return []

    return model.encode(

        chunks,

        convert_to_numpy=True,

        normalize_embeddings=True

    )


# ---------------------------------------------------------
# Generate Document Embeddings
# ---------------------------------------------------------

def generate_document_embeddings(chunks):

    if not chunks:

        return []

    texts = []

    for chunk in chunks:

        texts.append(
            chunk["text"]
        )

    embeddings = model.encode(

        texts,

        convert_to_numpy=True,

        normalize_embeddings=True

    )

    vector_records = []

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        vector_records.append(
            {
                "text": chunk["text"],
                "embedding": embedding,
                "metadata": chunk["metadata"]
            }
        )

    return vector_records