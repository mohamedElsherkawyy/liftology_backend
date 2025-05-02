from fastapi import APIRouter, HTTPException
from models import PlanRequest
from database import users_col
from ml.client import call_ml_model
from datetime import datetime

router = APIRouter()

@router.post("/generate/{user_email}")
async def generate_plan(req: PlanRequest, user_email: str):
    user = users_col.find_one({"user_info.email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await call_ml_model(req.dict())

    update_data = {
        "exercise_plan": {
            "input": req.dict(),
            "output": result,
            "timestamp": datetime.utcnow()
        }
        
    }

    users_col.update_one({"user_info.email": user_email}, {"$set": update_data})

    return {"status": "success", "plan": result}