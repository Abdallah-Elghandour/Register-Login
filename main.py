from fastapi import FastAPI
from src.routes import user


def create_app():
    app = FastAPI()
    app.include_router(user.user_router)
    app.include_router(user.guest_router)
    
    return app  

app = create_app()

@app.get("/")
async def root():
    return {"message": "Hello World"}

