import streamlit as st

from services.youtube_service import extract_video_id
from services.transcript_service import (
    get_transcript,
    transcript_to_text
)
from services.llm_service import summarize

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
                height=350
            )

            with st.spinner("Generating summary..."):

                summary = summarize(plain_text)

            st.subheader("📄 AI Summary")

            st.write(summary)