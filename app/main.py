from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import events
from app.db.database_connection import db_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_connection.connect()
    yield
    await db_connection.close()

app=FastAPI(lifespan=lifespan)




@app.get("/")
def root():
    return {"message":"Service is up!"}



app.include_router(router=events.router, prefix="/events")