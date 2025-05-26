from yt_dlp import YoutubeDL
from pathlib import Path
from Logging.logger import get_logger

logger = get_logger(__name__)


class SoundCloud:
    def __init__(self):
        self.DOWNLOAD_DIR = Path('download_soundcloud').resolve()
        self.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def download_audio(self, url: str):
        before_files = set(self.DOWNLOAD_DIR.glob('*.m4a'))

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": str(self.DOWNLOAD_DIR / "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                    "preferredquality": "192",
                },
                {"key": "FFmpegMetadata"}
            ],
            "quiet": True,
            "no_warnings": True,
            "ignoreerrors": True,
            "cachedir": False,
            "noplaylist": False,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception:
            return []

        after_files = set(self.DOWNLOAD_DIR.glob('*.m4a'))
        new_files = list(after_files - before_files)

        if not new_files:
            logger.warning("Could not find new files after upload.")

        return new_files
