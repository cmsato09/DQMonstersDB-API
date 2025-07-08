from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.app.routers import dqm1_endpoints

tags_metadata = [
    {
        "name": "dqm1 monsters",
        "description": "Monster list",
    },
    {
        "name": "dqm1 skills",
        "description": "Skills that monsters learn and inherit",
    },
    {
        "name": "dqm1 items",
        "description": "Useful items found in the game and their description",
    },
]

app = FastAPI(
    title="Dragon Quest Monsters Database API",
    description="API to get game information for the original DQMonsters "
    "gameboy game",
    version="1.0.0",
    openapi_tags=tags_metadata,
)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://dqmonsters-db.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(dqm1_endpoints.router)


@app.get("/")
def root():
    return {
        "message": ("Welcome to the DQMonsters API. " "Go to the Swagger UI interface")
    }
