from fastapi import FastAPI
from app.routes.sundae_routes import router as sundae_router

app = FastAPI(title="Sundae API", version="1.0")

# Register the sundae routes
app.include_router(sundae_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sundae API!"}
