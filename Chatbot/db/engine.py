
from sqlmodel import SQLModel, create_engine
from .models import User, Session, Conversation, Message

def get_engine(db_url: str):
    engine = create_engine(db_url, echo=False)
    SQLModel.metadata.create_all(engine)
    return engine
