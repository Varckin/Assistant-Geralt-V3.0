from yt_dlp import YoutubeDL
from pathlib import Path
from Logging.logger import get_logger

logger = get_logger(__name__)


class Youtube:
    def __init__(self, id: int):
        self.id_user = str(id)
        self.DOWNLOAD_DIR = Path(f'download_youtube/{self.id_user}').resolve()
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
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        after_files = set(self.DOWNLOAD_DIR.glob('*.m4a'))
        new_files = list(after_files - before_files)

        return new_files