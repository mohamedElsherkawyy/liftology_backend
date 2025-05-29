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
def update_full_plan(email: str, new_plan: str):
    try:
        plan_dict = json.loads(new_plan)
        plan_model = FullExercisePlan(**plan_dict)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON string")

    users_col.update_one(
        {"user_info.email": email},
        {"$set": {"exercise_plan": plan_model.dict()}}
    )

    return {"status": "success", "message": "Exercise plan updated successfully"}