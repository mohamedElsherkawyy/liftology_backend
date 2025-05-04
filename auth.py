from fastapi import APIRouter, HTTPException
from database import users_col
from models import UserRegister, UserLogin
import bcrypt

router = APIRouter()

@router.post("/signup")
def signup(user: UserRegister):
    # Check if email already exists
    if users_col.find_one({"user_info.email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Store user
    users_col.insert_one({
        "user_info": {
            "first_name": user.firstName,
            "last_name": user.lastName,
            "email": user.email,
            "password": hashed_password,
            "phone": user.phone,
            "country": user.country,
        },
        "exercise_plan": None,
        "diet_plan": None,
    })

    # Return success response
    return {
        "message": "User registered successfully",
        "first_name": user.firstName,
        "last_name": user.lastName,
        "email": user.email,
        "phone": user.phone,
        "country": user.country    
    }

@router.post("/login")
def login(data: UserLogin):
    # Find user by email
    user = users_col.find_one({"user_info.email": data.email})
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    stored_password = user["user_info"]["password"]
    if not bcrypt.checkpw(data.password.encode('utf-8'), stored_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Return success response
    return {
        "message": "Login successful",
        "first_name": user["user_info"]["first_name"],
        "last_name": user["user_info"]["last_name"],
        "email": user["user_info"]["email"],
        "phone": user["user_info"]["phone"],
        "country": user["user_info"]["country"],    
    }