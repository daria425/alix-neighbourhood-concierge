from fastapi import FastAPI
from app.routes.events import router as event_router
app=FastAPI()

@app.get("/")
def root():
    return {"message":"Service is up!"}

app.include_router(router=event_router, prefix="/events")