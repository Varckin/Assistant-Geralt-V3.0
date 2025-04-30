from yt_dlp import YoutubeDL
from pathlib import Path
from Logging.logger import get_logger
import asyncio
from aiogram.types import FSInputFile, Message

logger = get_logger(__name__)


class Youtube:
    def __init__(self):
        self.DOWNLOAD_DIR = Path('download_youtube').resolve()
        self.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    async def download_audio(self, url: str, message: Message):
        before_files = set(self.DOWNLOAD_DIR.glob('*.m4a'))
        def hook(d):
            after_files = set(self.DOWNLOAD_DIR.glob('*.m4a'))
            if before_files != after_files:
                new_files = list(after_files - before_files)
                print(new_files)
                asyncio.to_thread(
                    self.send_audio(message, new_files)
                )

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
            "progress_hooks": [hook],
            "quiet": True,
            "no_warnings": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    async def send_audio(self, message: Message, paths: list):
        for path in paths:
            try:
                await message.answer_audio(
                    audio=FSInputFile(path)
                )
                await asyncio.sleep(5)
                path.unlink()
            except Exception as e:
                await message.answer(f"Error: {e}")
                await asyncio.sleep(5)
                path.unlink()

# Добработать надо!!