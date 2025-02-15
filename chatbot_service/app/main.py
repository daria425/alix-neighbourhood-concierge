from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database_connection import db_connection
from app.routes import events
import os, asyncio
from dotenv import load_dotenv
load_dotenv()
subscription_name=os.getenv("PUBSUB_SUBSCRIPTION_NAME")
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_connection.connect()
    yield
    await db_connection.close()

app=FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message":"Chatbot service is up!"}

app.include_router(router=events.router, prefix="/events")