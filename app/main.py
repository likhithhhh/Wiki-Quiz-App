from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.routers.history_router import router as history_router
from app.routers.quiz_router import router as quiz_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.APP_NAME)

    # CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_ORIGIN, "http://localhost:5173", "http://localhost:3000","https://wiki-quiz-app-three.vercel.app/"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(quiz_router)
    app.include_router(history_router)

    @app.get("/health", tags=["health"])
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()


@app.on_event("startup")
def on_startup() -> None:
    # For this project we use simple metadata.create_all instead of Alembic migrations.
    Base.metadata.create_all(bind=engine)

