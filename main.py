from fastapi import FastAPI
from src.routes import user


def create_app():
    app = FastAPI()
    app.include_router(user.register_router)
    
    return app  

app = create_app()

@app.get("/")
async def root():
    return {"message": "Hello World"}

