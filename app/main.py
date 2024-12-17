from fastapi import FastAPI
from app.routes.sundae_routes import router as sundae_router

app = FastAPI(title="Stratyfy Ice Cream API")

# Include the routes for sundae-related operations
app.include_router(sundae_router)

@app.get("/")
def root():
    """Root endpoint to test if the API is running."""
    return {"message": "Welcome to the Ice Cream Parlor API!"}
