from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

class CustomValidationMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Ensure the middleware handles only HTTP requests
        if scope["type"] == "http":
            request = Request(scope, receive)

            try:
                # Call the next middleware or request handler
                response = await self.app(scope, receive, send)

                # Check if the response is valid and send it
                if response is not None:
                    await response(scope, receive, send)
            except ValidationError as exc:
                # Handle the ValidationError here
                response = JSONResponse(
                    status_code=422,
                    content={
                        "status": "error",
                        "errors": exc.errors(),
                        "message": "Validation error occurred"
                    }
                )
                await response(scope, receive, send)
            except Exception as exc:
                # Handle any other exceptions
                response = JSONResponse(
                    status_code=500,
                    content={"detail": "Internal server error"}
                )
                await response(scope, receive, send)
        else:
            await self.app(scope, receive, send) 
    # async def __call__(self, scope, receive, send):
    #     if scope["type"] == "http":
    #         request = Request(scope, receive)

    #         try:
    #                 # Call the next middleware or request handler
    #             response = await self.app(scope, receive, send)
    #             await response(scope, receive, send)
    #         except ValidationError as exc:
    #             # Handle the ValidationError here
    #             response = JSONResponse(
    #                 status_code=422,
    #                 content={
    #                 "is_success": False,
    #                 "result": exc.errors(),
    #                 "message": exc.errors(),
    #                 "status_code": 422
    #             }
    #             )
    #             await response(scope, receive, send)
    #     else:
    #         await self.app(scope, receive, send) 
