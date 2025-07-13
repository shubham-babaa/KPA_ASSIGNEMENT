from fastapi import FastAPI
from backend.routes import bogie, wheel
from backend.database import db_instance, Base  # import your singleton and base


app = FastAPI(
    title="KPA Form API",
    description="Assignment API for KPA form submission",
    version="1.0"
)


# app.include_router(user.router, prefix="/api/users", tags=["Users"],)
app.include_router(bogie.router, prefix="/api/forms", tags=["Bogie"])
app.include_router(wheel.router, prefix="/api/forms", tags=["Wheel"])

@app.get("/")
def root():
    return {"message": "KPA Form API is running."}

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=db_instance.engine)