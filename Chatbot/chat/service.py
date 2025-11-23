
from sqlmodel import Session as DBSession
from db.repos import ConversationRepo, MessageRepo
from db.models import Message
from ai.eden_client import EdenClient

class ChatService:
    def __init__(self, db: DBSession, eden: EdenClient):
        self.convs = ConversationRepo(db)
        self.msgs = MessageRepo(db)
        self.eden = eden

    def ensure_conversation(self, user_id, title="New chat"):
        convs = self.convs.list_by_user(user_id)
        return convs[0] if convs else self.convs.create(user_id, title=title)

    def send_user_message(self, conv_id, user_id, content: str):
        return self.msgs.add(Message(conversation_id=conv_id, user_id=user_id, role="user", content=content))

    def generate_reply(self, conv_id):
        history = self.msgs.list_by_conversation(conv_id)
        # Minimal prompt strategy (can upgrade to include selected history)
        messages = [{"role": m.role, "content": m.content} for m in history[-6:]] or [{"role": "system", "content": "You are a helpful assistant."}]
        assistant_text = self.eden.chat(messages)
        reply = self.msgs.add(Message(conversation_id=conv_id, role="assistant", content=assistant_text))
        return reply

    def full_turn(self, user_id, content: str):
        conv = self.ensure_conversation(user_id)
        self.send_user_message(conv.id, user_id, content)
        return self.generate_reply(conv.id), conv
