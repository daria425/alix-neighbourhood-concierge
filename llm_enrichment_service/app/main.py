from fastapi import FastAPI
from app.routes import recieve_pubsub
from contextlib import asynccontextmanager
from app.db.database_connection import db_connection


@asynccontextmanager
async def lifespan(app:FastAPI):
    await db_connection.connect()
    yield
    await db_connection.close()
    
app=FastAPI()

@app.get("/")
def root():
    return {"message":"LLM service is up!"}

app.include_router(recieve_pubsub.router, prefix="/recieve-pubsub")