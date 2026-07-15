from urllib.parse import urlparse, parse_qs


def extract_video_id(url):

    parsed_url = urlparse(url)

    # Standard: youtube.com/watch?v=VIDEO_ID
    query = parse_qs(parsed_url.query)
    if "v" in query:
        return query["v"][0]

    # Short link: youtu.be/VIDEO_ID
    if parsed_url.hostname and parsed_url.hostname.endswith("youtu.be"):
        video_id = parsed_url.path.lstrip("/")
        if video_id:
            return video_id

    # Shorts / embed: youtube.com/shorts/VIDEO_ID or youtube.com/embed/VIDEO_ID
    if parsed_url.path:
        parts = parsed_url.path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] in ("shorts", "embed"):
            return parts[1]

    return None