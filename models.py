from pydantic import BaseModel, EmailStr,Field
from typing import Optional, Dict, Any, Union, List

class UserRegister(BaseModel):
    First_name: str
    Last_name: str
    email: EmailStr
    password: str
    Phone_number: Optional [str] = None
    country: Optional [str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PlanRequest(BaseModel):
    weight: Union[int, float]
    height: Union[int, float]
    bmi: Union[int, float]
    body_fat_percentage: Union[int, float]
    gender: str
    age: int
    fitnessGoal:str
class chatRequest(BaseModel):
    user_input:str
    
<<<<<<< HEAD
class FullExercisePlan(BaseModel):
    output: Dict[str, Any]


class RecommendationParams(BaseModel):
    n_neighbors: int = 5
    return_distance: Optional[bool] = None

class FoodRecommendationRequest(BaseModel):
    nutrition_input: List[float]  # ← Flat list of 9 floats
    ingredients: Optional[List[str]] = Field(default_factory=list)
    params: RecommendationParams = Field(default_factory=RecommendationParams)
=======
class ExerciseUpdate(BaseModel):
    exercise: str
    sets: str
    reps: str
>>>>>>> 8d1d1dc61a7f5b85b565659bc67c06cdbcf52fb2
