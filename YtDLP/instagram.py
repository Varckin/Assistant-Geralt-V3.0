from pathlib import Path
from yt_dlp import YoutubeDL


class Instagram:
    def __init__(self, id: int):
        self.id_user = str(id)
        self.DOWNLOAD_DIR = Path(f'download_insta/{self.id_user}').resolve()
        self.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def is_instagram_url(url: str) -> bool:
        return any(sub in url for sub in ["instagram.com/reels/", "instagram.com/reel/", "instagram.com/p/", "instagram.com/tv/"])

    def download(self, url: str, filename_prefix: str = "download") -> Path | None:
        if not self.is_instagram_url(url):
            return None

        output_path = self.DOWNLOAD_DIR / f"{filename_prefix}.mp4"

        ydl_opts = {
            'cookiefile': str(Path('insta_cookies.txt')),
            'outtmpl': str(output_path),
            'format': 'mp4/best',
            'quiet': True,
            'noplaylist': True
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return output_path if output_path.exists() else None
        except Exception as e:
            return None
