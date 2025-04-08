from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from Logging.logger import get_logger
from Localization.localozation import get_str
from Cert.certificate import Certificate


logger = get_logger(__name__)
cert_router = Router()

@cert_router.message(Command("cert"))
async def cmd_cert(message: Message):
    try:
        cmd, domain = message.text.split(' ', 1)
        cert = Certificate()
        data = cert.fetch_cert(domain)
        path = cert.save_to_pdf(data, domain)

        file = FSInputFile(path, f"{domain}.pdf")
        await message.reply_document(file, caption=domain)
        
    except Exception as e:
        logger.error(e)
