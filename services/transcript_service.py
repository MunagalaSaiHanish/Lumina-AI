from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import IpBlocked


def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        return transcript

    except IpBlocked:
        return None


def transcript_to_text(transcript):

    full_text = ""

    for segment in transcript:
        full_text += segment.text + " "

    return full_text