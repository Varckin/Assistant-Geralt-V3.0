import requests
from Logging.logger import get_logger


logger = get_logger(__name__)

class PingService:
    def __init__(self, url: str):
        self.url: str = url

    def validator_url(self) -> None:
        if "http://" not in self.url or "https://" not in self.url:
            self.url = "http://" + self.url

    def ping(self) -> str:
        self.validator_url()
        try:
            response = requests.get(url=self.url, timeout=5)
            return f"Status: {str(response.status_code)}"

        except requests.exceptions.RequestException as e:
            logger.error(e)
            return "Error using"
