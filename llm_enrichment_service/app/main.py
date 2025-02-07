from fastapi import FastAPI
from app.routes import recieve_pubsub
app=FastAPI()



@app.get("/")
def root():
    return {"message":"LLM service is up!"}

app.include_router(recieve_pubsub.router, prefix="/recieve-pubsub")