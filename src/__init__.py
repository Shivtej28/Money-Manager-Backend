from fastapi import FastAPI, Request, HTTPException
from src.routers import user, categories, banks, transaction
from .models import data_model
from .dao.database import engine
from fastapi.responses import JSONResponse
from src.utils.middleware.custom_validation_middleware import CustomValidationMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import ExceptionMiddleware

class MyHTTPException(HTTPException):
    pass

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    result = [error.get('msg') for error in exc.errors()]
    print(result)
    return JSONResponse(
                    status_code=400,
                    content={
                    "is_success": False,
                    "result": result,
                    "message": exc.errors()[0].get("msg"),
                    "status_code": 422
                }
                )

def create_app():
    app = FastAPI()
    data_model.Base.metadata.create_all(engine)
    # app.add_middleware(CustomValidationMiddleware)

    app.add_exception_handler(RequestValidationError, handler=validation_exception_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins (for development purposes)
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(user.router)
    app.include_router(categories.router)
    app.include_router(banks.router)
    return app
