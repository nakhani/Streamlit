# db/repos.py
from datetime import datetime, timedelta
from typing import Optional, List
from sqlmodel import Session as DBSession, select
from .models import User, Session, Conversation, Message
import secrets

class UserRepo:
    def __init__(self, db: DBSession): self.db = db
    def by_email(self, email: str) -> Optional[User]:
        return self.db.exec(select(User).where(User.email == email)).first()
    def by_username(self, username: str) -> Optional[User]:
        return self.db.exec(select(User).where(User.username == username)).first()
    def create(self, user: User) -> User:
        self.db.add(user); self.db.commit(); self.db.refresh(user); return user

class SessionRepo:
    def __init__(self, db: DBSession): self.db = db
    def new(self, user_id, ttl_hours=24) -> Session:
        token = secrets.token_urlsafe(32)
        sess = Session(user_id=user_id, token=token,
                       expires_at=datetime.utcnow() + timedelta(hours=ttl_hours))
        self.db.add(sess); self.db.commit(); self.db.refresh(sess); return sess
    def by_token(self, token: str) -> Optional[Session]:
        return self.db.exec(select(Session).where(Session.token == token)).first()
    def delete(self, token: str): 
        s = self.by_token(token); 
        if s: self.db.delete(s); self.db.commit()

class ConversationRepo:
    def __init__(self, db: DBSession): self.db = db
    def create(self, user_id, title="Untitled") -> Conversation:
        c = Conversation(user_id=user_id, title=title)
        self.db.add(c); self.db.commit(); self.db.refresh(c); return c
    def list_by_user(self, user_id) -> List[Conversation]:
        return self.db.exec(select(Conversation).where(Conversation.user_id==user_id)).all()

class MessageRepo:
    def __init__(self, db: DBSession): self.db = db
    def add(self, msg: Message) -> Message:
        self.db.add(msg); self.db.commit(); self.db.refresh(msg); return msg
    def list_by_conversation(self, conv_id) -> List[Message]:
        return self.db.exec(select(Message).where(Message.conversation_id==conv_id).order_by(Message.created_at)).all()
