import streamlit as st

from services.youtube_service import extract_video_id
from services.transcript_service import (
    get_transcript,
    transcript_to_text
)
from services.chunk_service import chunk_text
from services.llm_service import summarize
from services.embedding_service import generate_embeddings

st.set_page_config(
    page_title="AI Video Analyzer",
    page_icon="🎥",
    layout="centered"
)

st.title("🎥 AI Video Analyzer")

st.write("Paste a YouTube URL")

video_url = st.text_input("YouTube URL")

if st.button("Analyze Video"):

   
    video_id = extract_video_id(video_url)

    if video_id is None:
        st.error("Invalid YouTube URL")

    else:

       
        raw_transcript = get_transcript(video_id)

        if raw_transcript is None:

            st.warning(
                "Transcript couldn't be fetched. "
                "YouTube may have blocked the request."
            )

        else:

          
            plain_text = transcript_to_text(raw_transcript)

            st.success("✅ Transcript Loaded!")

            st.text_area(
                label="Transcript",
                value=plain_text,
                height=300
            )

            
            chunks = chunk_text(plain_text)

            st.subheader("📦 Chunks")

            st.write(f"Total Chunks : {len(chunks)}")

            for i, chunk in enumerate(chunks):

                with st.expander(f"Chunk {i+1}"):

                    st.write(chunk)
                    

                    embeddings = generate_embeddings(chunks)

                st.subheader("Embeddings")

                st.write(f"Total Embeddings: {len(embeddings)}")

                st.write("Dimension of one embedding:")

                st.write(len(embeddings[0]))
           
            with st.spinner("Generating Summary..."):

                summary = summarize(plain_text)

            st.subheader("📝 Summary")

            st.write(summary)

            