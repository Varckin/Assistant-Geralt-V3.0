from Models.configDB import async_session
from Models.models import User
from sqlalchemy.future import select
from Logging.logger import get_logger
from json import load
from pathlib import Path


logger = get_logger(__name__)

async def get_land(user_id: int) -> str:
    try:
        async with async_session() as session:
            result = await session.execute(
                select(User).filter_by(user_id=user_id)
            )
            user = result.scalar()

            return user.language_code
        
    except Exception as e:
        logger.error(e)

async def get_str(user_id: int, key_str: str) -> str:
    try:
        lang_code: str = await get_land(user_id)
        if Path(f"{str(Path.cwd())}/Localization/{lang_code}.json").is_file():
            localization: dict = await json_read(f"{str(Path.cwd())}/Localization/{lang_code}.json")
            return localization.get(key_str)
        else:
            localization: dict = await json_read(f"{str(Path.cwd())}/Localization/en.json")
            return localization.get(key_str)
    except (KeyError, FileNotFoundError) as e:
        logger.critical(e)

async def json_read(file_name: str) -> dict:
    with open(file_name, 'r', encoding='utf-8') as file:
        data: dict = load(file)
        return data
