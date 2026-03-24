# ## Exercice 1: Modèle Utilisateur Basique

# **Énoncé**:
# Créez un modèle Pydantic `User` avec:
# - `id`: entier (non modifiable)
# - `username`: chaîne (2-50 caractères)
# - `email`: email valide
# - `age`: entier optionnel (0-150 si fourni)
# - `is_active`: booléen (par défaut True)

# Testez avec une route POST `/users` qui accepte le modèle.

from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="FastAPI Hello World Demo",
    description="Simple FastAPI application with automatic documentation",
    version="1.0.0"
)

class User(BaseModel):
    """User model"""
    id: int
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(..., gt=0, le=150)
    is_active: bool = True
    
    
@app.post("/users", response_model=User, status_code=201, tags=["users"])
async def create_user(user: User):
    return user
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)