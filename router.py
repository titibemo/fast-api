from fastapi import APIRouter, FastAPI
import uvicorn
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from pydantic_settings import BaseSettings
from enum import Enum
from datetime import datetime

# TODO docs https://fastapi.tiangolo.com/reference/apirouter/#fastapi.APIRouter.include_router

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
exercice_4 = APIRouter()
exercice_5 = APIRouter()
exercice_6 = APIRouter()
exercice_7 = APIRouter()

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
    
# exercice 4
class Item(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    total: Optional[float]
    
    @model_validator(mode='after')
    def calculate_total(self):
        self.total = self.quantity * self.price
        return self

class Order(BaseModel):
    order_id: str
    customer_email: EmailStr
    items: list[Item]
    
    @model_validator(mode='after')
    def validate_items(self):
        if not self.items:
            raise ValueError("Order must have at least one item")
        return self
    
# exercice 5
class ApiResponse(BaseModel):
    success: bool
    data: dict
    message: str
    timestamp: str
    
    @model_validator(mode='after')
    @classmethod
    def add_timestamp(cls, values):
        values.timestamp = datetime.now().isoformat()
        return values
    
# exercice 6 TODO
class Settings(BaseSettings):
    app_name: str = Field(..., env='APP_NAME')
    debug: bool = Field(False, env='DEBUG')
    database_url: str = Field(..., env='DATABASE_URL')
    secret_key: str = Field(..., env='SECRET_KEY')
    api_v1_prefix: str = Field("/api/v1", env='API_V1_PREFIX')

# exercice 7
# **Énoncé**:
# Créez un modèle `Événement` avec:
# - `type`: "online" ou "offline"
# - `title`: titre (requis)
# - `location`: obligatoire si type="offline", sinon facultatif
# - `url`: obligatoire si type="online", sinon facultatif
# - `max_participants`: entier (>= 1)

# **Indices**:
# - Utilisez `model_validator` pour la logique conditionnelle
# - Accédez à `self.type` pour vérifier le type
# - Levez `ValueError` si la validation échoue
class TypeCategory(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"

class Event(BaseModel):
    type: TypeCategory
    title: str = Field(..., min_length=2, max_length=50)
    location: Optional[str]
    url: Optional[str]
    max_participants: int = Field(..., gt=0)

    @model_validator(mode='after')
    def validate_type(self):
        if self.type == TypeCategory.OFFLINE and not self.location:
            raise ValueError("Location is required for offline events")
        if self.type == TypeCategory.ONLINE and not self.url:
            raise ValueError("URL is required for online events")
        return self
    
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

# route exo 4
@exercice_4.post("/orders", response_model=Order, status_code=201, tags=["orders"])
async def create_order(order: Order):
    return order

# route exo 5
@exercice_5.post("/api_response", response_model=ApiResponse, status_code=201, tags=["api_response"])
async def create_api_response(api_response: ApiResponse):
    return api_response

# route exo 6
@exercice_6.post("/settings", response_model=Settings, status_code=201, tags=["settings"])
async def create_settings(settings: Settings):
    return settings

# route exo 7
@exercice_7.post("/events", response_model=Event, status_code=201, tags=["events"])
async def create_event(event: Event):
    return event

# router

internal_router.include_router(exercice_1)
internal_router.include_router(exercice_2)
internal_router.include_router(exercice_3)
internal_router.include_router(exercice_4)
internal_router.include_router(exercice_5)
internal_router.include_router(exercice_6)
internal_router.include_router(exercice_7)
app.include_router(internal_router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
