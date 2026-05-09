from fastapi import APIRouter

from app.api.routes import analytics, auth, locations, predict, stats, users, ws


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(predict.router, prefix="/predict", tags=["prediction"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(ws.router, tags=["ws"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

