import requests, re
from Logging.logger import get_logger


logger = get_logger(__name__)

class PingService:
    def __init__(self, url: str):
        self.url: str = url

    def validator_url(self) -> None:
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            self.url = "https://" + self.url
        elif self.url.startswith("http://"):
            self.url = re.sub('http://', 'https://', self.url)

    def ping(self) -> str:
        self.validator_url()
        try:
            response = requests.get(url=f"{self.url}:443", timeout=5)
            return f"Status: {str(response.status_code)}"

        except requests.exceptions.RequestException as e:
            logger.error(e)
            return "Service not avalible"
