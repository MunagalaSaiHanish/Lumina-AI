import streamlit as st

from services.youtube_service import extract_video_id
from services.transcript_service import (
    get_transcript,
    transcript_to_text
)
from services.chunk_service import chunk_text
from services.embedding_service import generate_embeddings
from services.vector_store import (
    create_vector_store,
    retrieve_chunks
)
from services.llm_service import (
    summarize,
    ask_question
)

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🎥",
    layout="wide"
)

# ----------------------------------------------------
# SESSION STATE
# ----------------------------------------------------

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

with st.sidebar:

    st.title("🎥 AI Knowledge Assistant")

    st.markdown("---")

    st.subheader("About")

    st.write("""
This application uses Retrieval-Augmented Generation (RAG)
to analyze YouTube videos.

Pipeline

• Transcript

• Chunking

• Embeddings

• FAISS

• Qwen
""")

    st.markdown("---")

    st.success("✅ RAG Enabled")

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.title("🎥 AI Knowledge Assistant")

st.caption(
    "Analyze YouTube videos using AI"
)

st.divider()

# ----------------------------------------------------
# INPUT
# ----------------------------------------------------

video_url = st.text_input(
    "🔗 Paste YouTube URL"
)

# ----------------------------------------------------
# ANALYZE
# ----------------------------------------------------

if st.button(
    "🚀 Analyze Video",
    use_container_width=True
):

    video_id = extract_video_id(video_url)

    if video_id is None:

        st.error("Invalid YouTube URL")

    else:

        with st.spinner("Fetching Transcript..."):

            raw_transcript = get_transcript(video_id)

        if raw_transcript is None:

            st.error(
                "Couldn't fetch transcript."
            )

        else:

            plain_text = transcript_to_text(raw_transcript)

            st.session_state.transcript = plain_text

            with st.spinner("Generating Summary..."):

                summary = summarize(plain_text)

            st.session_state.summary = summary

            with st.spinner("Building Knowledge Base..."):

                chunks = chunk_text(plain_text)

                embeddings = generate_embeddings(chunks)

                vector_store = create_vector_store(
                    embeddings
                )

            st.session_state.chunks = chunks

            st.session_state.vector_store = vector_store

            st.success(
                "✅ Video Analysis Complete!"
            )

# ----------------------------------------------------
# TRANSCRIPT
# ----------------------------------------------------

if st.session_state.transcript:

    st.divider()

    st.subheader("📜 Video Transcript")

    st.text_area(
        "",
        st.session_state.transcript,
        height=350
    )

# ----------------------------------------------------
# SUMMARY
# ----------------------------------------------------

if st.session_state.summary:

    st.divider()

    st.subheader("📄 Executive Summary")

    st.write(st.session_state.summary)

# ----------------------------------------------------
# CHAT
# ----------------------------------------------------

if st.session_state.vector_store is not None:

    st.divider()

    st.subheader("💬 Ask Anything About This Video")

    question = st.text_input(
        "Your Question"
    )

    if st.button(
        "Ask AI",
        use_container_width=True
    ):

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching Knowledge Base..."
            ):

                retrieved_chunks = retrieve_chunks(
                    question,
                    st.session_state.vector_store,
                    st.session_state.chunks
                )

                context = "\n\n".join(
                    retrieved_chunks
                )

            with st.spinner(
                "Generating Answer..."
            ):

                answer = ask_question(
                    question,
                    context
                )

            st.subheader("🤖 AI Answer")

            st.write(answer)