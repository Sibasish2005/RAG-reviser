from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


ytt_api = YouTubeTranscriptApi()


def get_video_id(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname in ("youtube.com", "www.youtube.com"):
        return parse_qs(parsed_url.query).get("v", [None])[0]

    if parsed_url.hostname in ("youtu.be", "www.youtu.be"):
        return parsed_url.path.strip("/").split("/")[0]

    if parsed_url.path.startswith("/shorts/"):
        return parsed_url.path.split("/")[2]

    return None


def transcribe(url):
    video_id = get_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL")

    transcript = ytt_api.fetch(
        video_id,
        languages=["en-US", "en", "hi", "bn"]
    )

    return " ".join(snippet.text for snippet in transcript)




