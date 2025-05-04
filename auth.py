from fastapi import APIRouter, HTTPException
from database import users_col
from models import UserRegister, UserLogin

router = APIRouter()

@router.post("/signup")
def signup(user: UserRegister):
    if users_col.find_one({"user_info.email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    users_col.insert_one({
        "user_info":{
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "password": user.password,
        "phone": user.phone,
        "country": user.country,
            },
        "exercise_plan": None ,
        "diet_plan": None,
    })
    return {"message": "User registered successfully",
        "firstName": user["user_info"]["firstName"],
        "lastName": user["user_info"]["lastName"],
        "email": user["user_info"]["email"],
        "phone": user["user_info"]["phone"],
        "country": user["user_info"]["country"],    
            }

@router.post("/login")
def login(data: UserLogin):
    user = users_col.find_one({"user_info.email": data.email})
    if not user or user["user_info"]["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "message": "Login successful",
        "first_name": user["user_info"]["first name"],
        "last_name": user["user_info"]["last name"],
        "email": user["user_info"]["email"],
        "phone_number": user["user_info"]["phone number"],
        "country": user["user_info"]["country"],    
    }
