from fastapi import FastAPI
from auth import router as auth_router
from routes.plans import router as plans_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(plans_router)

@app.get("/")
def root():
    return {"message": "Liftology Backend is running!"}

