# ConnectionManager class will have connect, disconnect, send_message, send_text, active_connections Dict[int, WebSocket]
from datetime import datetime
from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import json
import chatservice as chatservice
from security import verify_token
from database import get_db
from sqlalchemy.orm import Session
from models import User, Product, ChatHistory
from chatservice import process_message
# (
#    1: Websocket, # user_id: websocket,
#    2: Websocket,
#    3: Websocket,
# )
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected")

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"User {user_id} disconnected")

    async def send_message(self, user_id: int, message: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def send_text(self, message: str, user_id: int):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_text(message)

manager = ConnectionManager()

# authenticate websocket
async def authenticate_websocket(token: str) -> int:
    user_id = verify_token(token)
    if user_id:
        return user_id
    else:
        raise Exception("Invalid or expired token")
       
# load chat history by user id from database and return list of chat history
# [{"sender": "user", "message": "Hello", "timestamp": "2024-01-01T12:00:00Z}]
async def load_chat_history(user_id: int, db: Session, limit: int = 50) -> List[dict]:
    chat_history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp.desc()).limit(limit).all()
    if not chat_history:
        return None
    #reverse
    chat_history.reverse()
    # list of {"sender": "user", "message": "Hello", "timestamp": "2024-01-01T12:00:00"}
    chat_messages = []
    for message in chat_history:
        message = {
            "sender": "user" if message.sender == "user" else "assistant",
            "message": message.message, 
            "timestamp": str(message.timestamp.isoformat())
        }  
        chat_messages.append(message)

    return chat_messages

# handle-chat_websocket will receive websocket connection, authenticate user, and manage connection
# 1. authenticate
# 2. retrieve user details from database
# 3. add user to connection manager
# 4. retrieve user chat history
# 5. send chat history to user
# 6. wait for user messages.
# 7. save user messages to database
# 8. process message and get response from chatbot
# 9. save bot response to database
# 10. send bot response to user
# 11. wait for next user message

async def handle_chat_websocket(websocket: WebSocket, token: str = Query(...)):
     try:
        user_id = await authenticate_websocket(token)
        # fetch user details from database
        db: Session = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
           await websocket.close(code=1008, reason="Invalid user")
           return

        await manager.connect(websocket, user_id)
        chat_history = await load_chat_history(user_id, db)

        if chat_history:
            print(f"Loaded chat history for user {user_id}: {chat_history}")
            history_message = {"type": "history", "message": chat_history}
            await manager.send_message(history_message, user_id)
        else: 
            welcome_text = f"Hi {user.full_name}, welcome to {chatservice.company_name}. I am {chatservice.bot_name}, How can I help you?",
            welcome_message = {"type": "message", "message": welcome_text, "sender": "Assistant", "timestamp": str(datetime.now())}
            await save_message_to_db(user_id, welcome_text, "assistant", db)
            await manager.send_message(welcome_message, user_id)
#wait for user messages
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message = message_data["message"].strip()
            if not message:
                continue
            # save user message to database
            await save_message_to_db(user_id, message, "user", db)
            # process message and get response from chatbot
            # retrieve products list
            products = db.query(Product).all()
            product_list = [product.name for product in products]

            # get recent chat history
            chat_history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp.desc()).limit(10).all()
            
            # reverse
            chat_history.reverse()

            response = chatservice.chat(user.full_name, message, product_list, chat_history)
            # save bot response to database
            await save_message_to_db(user_id, response, "assistant", db)
            # send bot response to user
            response_message = {"type": "message", "message": response, "sender": "Assistant", "timestamp": str(datetime.now())}
            await manager.send_message(response_message, user_id)

     except WebSocketDisconnect:
            manager.disconnect(user_id)
            print(f"User disconnected: {user_id}")
            try:
                await websocket.close()
            except:
                pass
            if user_id :
                del manager.active_connections[user_id]

     except Exception as e:
        print(f"Error occurred: {e}")
     finally:
         await db.close()

# save_message_to_db
async def save_message_to_db(user_id: int, message: str, sender: str, db: Session):
    chat_history = ChatHistory(user_id=user_id, message=message, sender=sender)
    db.add(chat_history)
    db.commit()
    db.refresh(chat_history)
    return chat_history