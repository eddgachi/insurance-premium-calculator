from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

from app.routes import router as prem_router

origins = [
    "http://localhost:5173",
]


app = FastAPI()
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prem_router)

desc = ""


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_description = f"{desc}\n\n\nmade with ❤️"

    openapi_schema = get_openapi(
        title="Insurance Premium Calculator - Backend APIs",
        version="1.1.0",
        description=openapi_description,
        routes=app.routes,
    )

    # Ensure "components" key exists
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
