from fastapi import APIRouter, HTTPException
from models import PlanRequest,FullExercisePlan
from database import users_col
from ml.client import call_ml_model
from datetime import datetime
import json
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

@router.put("/update-exercise-plan/{email}")
def update_full_plan(email: str, new_plan: FullExercisePlan):
    user = users_col.find_one({"user_info.email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_plan=json.loads(new_plan)
    users_col.update_one(
        {"user_info.email": email},
        {"$set": {"exercise_plan": new_plan}}
    )

    return {"status": "success", "message": "Exercise plan updated successfully"}