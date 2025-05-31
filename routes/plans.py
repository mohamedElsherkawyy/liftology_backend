from fastapi import APIRouter, HTTPException
from models import PlanRequest,ExerciseUpdate
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

@router.put("/exercise-plan/{email}/{day}/{exercise_number}")
def update_exercise(email: str, day: str, exercise_number: str, update: ExerciseUpdate):
    user = users_col.find_one({"user_info.email": email})
    if not user or "exercise_plan" not in user:
        raise HTTPException(status_code=404, detail="User or exercise plan not found")

    plan = user.get("exercise_plan", {}).get("output", {}).get("plan", {})

    if day not in plan:
        raise HTTPException(status_code=404, detail=f"{day} not found in plan")

    if exercise_number not in plan[day]:
        raise HTTPException(status_code=404, detail=f"Exercise {exercise_number} not found on {day}")

    # Update in memory
    plan[day][exercise_number]["exercise"] = update.exercise
    plan[day][exercise_number]["sets"] = update.sets
    plan[day][exercise_number]["reps"] = update.reps

    # Write back to DB
    users_col.update_one(
        {"user_info.email": email},
        {"$set": {"exercise_plan.output.plan": plan}}
    )

    return {"status": "success", "message": f"Exercise {exercise_number} on {day} updated"}
