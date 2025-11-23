
from sqlmodel import Session as DBSession
from db.repos import UserRepo, SessionRepo
from db.models import User
from .hashing import hash_password, verify_password

class AuthService:
    def __init__(self, db: DBSession):
        self.users = UserRepo(db)
        self.sessions = SessionRepo(db)

    def register(self, email: str, username: str, password: str) -> User:
        if self.users.by_email(email) or self.users.by_username(username):
            raise ValueError("Email or username already exists")
        user = User(email=email, username=username, password_hash=hash_password(password))
        return self.users.create(user)

    def login(self, email_or_username: str, password: str):
        user = self.users.by_email(email_or_username) or self.users.by_username(email_or_username)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        return self.sessions.new(user.id)

    def validate_token(self, token: str):
        sess = self.sessions.by_token(token)
        if not sess or sess.expires_at <= __import__("datetime").datetime.utcnow():
            return None
        return sess
