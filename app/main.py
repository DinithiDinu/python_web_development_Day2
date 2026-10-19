from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import departments, employees
from app.core.exceptions import AppError
from app.database.database import Base, engine
from app.models import models  

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management API")


@app.exception_handler(AppError)
def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(departments.router)
app.include_router(employees.router)