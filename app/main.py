import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.errors import ErrorResponse
from app.resources import organizations, offices, radar_data

root_path = os.environ.get("ROOT_PATH", "")

app = FastAPI(
    title="AMA HOI API",
    description="""API for managing work station availability in offices.
    A typical use case is that an office admin can decide the number work stations that should be available.
    Then in the other end a normal employee can check whether there are any available work stations across multiple offices before
    deciding where to work for the day""",
    version="0.1.0",
    root_path=root_path,
)

origins = [
    "*",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(organizations.router, prefix="/organizations")

app.include_router(offices.router, prefix="/offices")

app.include_router(radar_data.router, prefix="/radar-data")


@app.get("/openapi")
def openapi():
    return app.openapi()


@app.exception_handler(ErrorResponse)
def abort_exception_handler(request: Request, exc: ErrorResponse):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})
