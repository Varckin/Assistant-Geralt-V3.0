import os

from Models.configDB import async_session
from Models.models import User
from sqlalchemy.future import select
from Logging.logger import get_logger


logger = get_logger(__name__)

class AdminPanel:
    def __init__(self):
        self.admin_id: str = os.getenv('ADMIN_ID')

    def check_admin_id(self, user_id: int) -> bool:
        if self.admin_id == str(user_id):
            return True
        else:
            return False
    
    async def check_premium_user(self, user_id: int) -> bool:
        try:
            async with async_session() as session:
                result = await session.execute(select(User).filter_by(user_id=user_id))
                user = result.scalar()

                return user.premium
        
        except Exception as e:
            logger.error(e)

    async def how_many_users_total(self) -> str:
        try:
            async with async_session() as session:
                result = await session.execute(select(User))
                users = result.scalars().all()

                return str(len(users))
        
        except Exception as e:
            logger.error(e)

    async def show_all_users(self) -> str:
        try:
            async with async_session() as session:
                result = await session.execute(select(User))
                users = result.scalars().all()
                text: str = "List Users:\n"

                for user in users:
                    text += f"""
id: {user.id}
user id: `{user.user_id}`
username: `{user.username}`
name: `{user.first_name}`
follow: `{user.create_at}`
premium: `{user.premium}`
"""
                return text
        
        except Exception as e:
            logger.error(e)
            return 'Users not find'
