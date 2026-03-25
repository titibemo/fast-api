from fastapi import APIRouter, FastAPI
import uvicorn
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from enum import Enum


app = FastAPI(
    title="Test router",
    description="Simple FastAPI application with automatic documentation",
    version="1.0.0"
)

app = FastAPI()
internal_router = APIRouter()
exercice_1 = APIRouter()
exercice_2 = APIRouter()
exercice_3 = APIRouter()

############################################################ CLASS ->

# exercice 1
class User(BaseModel):
    """User model"""
    id: int
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(None, gt=0, le=150)
    is_active: bool = True
    
# exercice 2
class Password(BaseModel):
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if not any(char.islower() for char in value):
            raise ValueError("password must contain at least one lowercase letter")
        if not any(char.isupper() for char in value):
            raise ValueError("password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("password must contain at least one digit")
        if not any(char in "!@#$%^&*()_+-=" for char in value):
            raise ValueError("password must contain at least one special character")
        return value
    
    @model_validator(mode='after')
    def validate_passwords_match(self):
        """
        Root validator - validate across multiple fields
        Checks that password and confirm_password match
        """
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self
    
# exercice 3

class Category(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    OTHER = "other"

class Supplier(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: Optional[str]

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0)
    category: Category
    stock: int = Field(..., ge=0)
    supplier: Supplier
    
############################################################

######################### routes ->

# route exo 1
@exercice_1.post("/users", response_model=User, status_code=201, tags=["users"])
async def create_user(user: User):
    return user

# route exo 2
@exercice_2.post("/password", response_model=Password, status_code=201, tags=["password"])
async def create_password(password: Password):
    return password

# route exo 3
@exercice_3.post("/products", response_model=Product, status_code=201, tags=["products"])
async def create_product(product: Product):
    return product

internal_router.include_router(exercice_1)
internal_router.include_router(exercice_2)
internal_router.include_router(exercice_3)
app.include_router(internal_router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)