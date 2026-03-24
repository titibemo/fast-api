## Exercice 2: Validateurs Personnalisés

# **Énoncé**:
# Créez un modèle `Password` avec validation:
# - `password`: au moins 8 caractères, doit contenir minuscule, majuscule, chiffre, symbole
# - `confirm_password`: doit égaler `password`

# Retournez des erreurs détaillées si la validation échoue.

# Exemple:
# ```bash
# # Valide
# {"password": "SecurePass123!", "confirm_password": "SecurePass123!"}

# # Invalide
# {"password": "weak", "confirm_password": "weak"}
# # Erreur: "password too short"
# ```
 
from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator

app = FastAPI(
    title="FastAPI Hello World Demo",
    description="Simple FastAPI application with automatic documentation",
    version="1.0.0"
)

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
    
@app.post("/password", response_model=Password, status_code=201, tags=["password"])
async def create_password(password: Password):
    return password
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)