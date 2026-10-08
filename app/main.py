
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.database import engine, Base
from app import models

from app.routes import auth
from app.routes import doctors
from app.routes import patients


# Create database tables
Base.metadata.create_all(bind=engine)


# Logging
logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# Create FastAPI application
app = FastAPI(
    title="Doctor Patient Management API",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home endpoint
@app.get("/")
def home():
    logger.info("Home endpoint was accessed")

    return {
        "message": "Doctor Patient API is running"
    }


# Authentication routes FIRST
app.include_router(
    auth.router
)


# Doctor routes
app.include_router(
    doctors.router,
    prefix="/api/v1"
)


# Patient routes
app.include_router(
    patients.router,
    prefix="/api/v1"
)