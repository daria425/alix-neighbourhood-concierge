from fastapi import FastAPI
from app.routes import events
app=FastAPI()

@app.get("/")
def root():
    return {"message":"Service is up!"}

app.include_router(router=events.router, prefix="/events")