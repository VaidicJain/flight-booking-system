from fastapi import FastAPI
from routers.users import auth_router

version = "v1"
app = FastAPI(
    title="Aero Bound Ventures Backend",
    description="Backend for Aero Bound Ventures",
    version=version,
)

app.include_router(auth_router, tags=["users"], prefix=f"/api/{version}/auth")


@app.get("/")
def hello():
    return {"message": "Hello, World!"}
