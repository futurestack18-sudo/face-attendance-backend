from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth_routes, register, attendance

app = FastAPI(title="Face Attendance System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(register.router)
app.include_router(attendance.router)

@app.get("/")
def home():
    return {"message": "Backend running successfully"}

@app.get("/health")
def health():
    return {"status": "healthy"}