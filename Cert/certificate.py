import requests, os
from Logging.logger import get_logger
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


logger = get_logger(__name__)

class Certificate:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        self.url: str = os.getenv('URL_CRT')
        self.path = BASE_DIR / 'tmp' / 'pdf'
        self.path.mkdir(parents=True, exist_ok=True)

    def fetch_cert(self, domain: str) -> list:
        full_url: str = self.url.format(domain=domain)
        response = requests.get(full_url)

        if response.status_code != 200:
            logger.info(f"{domain} -- {response.status_code}")
            return []
        
        try:
            json_data = response.json()
            return json_data
        except Exception as e:
            logger.error(e)
            return []
        
    def save_to_pdf(self, json_data: list, domain: str) -> str:
        self.check_files()
        full_path: str = f"{str(self.path)}/{domain}.pdf"
        c = canvas.Canvas(filename=full_path, pagesize=letter)
        width, height =  letter

        textobject = c.beginText()
        textobject.setTextOrigin(40, height - 40)
        textobject.setFont("Helvetica", 10)

        textobject.textLine(f"Certificate for domain: {domain}")
        textobject.textLine(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        textobject.textLine("")
        textobject.textLine("")

        for i, cert in enumerate(json_data, 1):
            cn = cert.get("common_name", cert.get("name_value", "N/A"))
            textobject.textLine(f"{i}. CN: {cn}")
            for key, value in cert.items():
                textobject.textLine(f"      {key}: {value}")
            textobject.textLine("")

            if textobject.getY() < 60:
                c.drawText(textobject)
                c.showPage()
                textobject = c.beginText()
                textobject.setTextOrigin(40, height - 40)
                textobject.setFont("Helvetica", 10)

        c.drawText(textobject)
        c.save()
        return full_path

    def check_files(self):
        files = [f for f in self.path.iterdir() if f.is_file()]
        if len(files) > 40:
            logger.info(f"In folder {self.path} {len(files)} files, i delete all...")
            for file in files:
                try:
                    file.unlink()
                except Exception as e:
                    logger.error(e)
        else:
            logger.info(f"In folder - {len(files)} files, dont delete...")
