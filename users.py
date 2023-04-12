from database.models import User
from fastapi_sqlalchemy import db

async def get_user(name: str):
    selected_user = db.session.query(User).filter(User.name == name).first()
    if not selected_user:
        raise Exception("user not found")
    return selected_user
