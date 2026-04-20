from fastapi import FastAPI, Depends, HTTPException, WebSocket, status
from docs.authentication import authentication_router
from docs.database import BaseModel, engine
from docs.my_orders import my_orders_router
from docs.chat_websocket import handle_chat_websocket
from fastapi.middleware.cors import CORSMiddleware
from docs.products import products_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

BaseModel.metadata.create_all(bind=engine)

app.include_router(authentication_router)
app.include_router(my_orders_router)
app.include_router(products_router)

@app.get("/")
async def root():
    return FileResponse("chat_web_ui/login.html")

@app.get("/login")
async def login():
    return FileResponse("chat_web_ui/login.html")

@app.get("/signup")
async def signup():
    return FileResponse("chat_web_ui/signup.html")

@app.get("/chat")
async def chat():
    return FileResponse("chat_web_ui/chat.html")

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await handle_chat_websocket(websocket, token)