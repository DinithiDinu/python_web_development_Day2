import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import departments, employees
from app.core.exceptions import AppError
from app.core.logging_config import setup_logging
from app.database.database import Base, engine
from app.models import models  # noqa: F401

setup_logging()
logger = logging.getLogger("employee_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("Application started")
    yield


app = FastAPI(
    title="Employee Management API",
    description="Manage departments, employees and leave records.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration,
        },
    )
    return response


@app.exception_handler(AppError)
def app_error_handler(request: Request, exc: AppError):
    logger.warning(exc.message, extra={"path": request.url.path, "status_code": exc.status_code})
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(Exception)
def unexpected_error_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(departments.router)
app.include_router(employees.router)