# ## Exercice 3: Modèles Imbriqués

# **Énoncé**:
# Créez une structure pour un `Produit` contenant:
# - `name`: nom du produit
# - `price`: prix (> 0)
# - `category`: catégorie (énumération: ELECTRONICS, CLOTHING, FOOD, OTHER)
# - `stock`: entier (>= 0)
# - `supplier`: objet Pydantic avec:
#   - `name`: nom du fournisseur
#   - `email`: email du fournisseur
#   - `phone`: téléphone (optionnel)

from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

app = FastAPI(
    title="FastAPI Hello World Demo",
    description="Simple FastAPI application with automatic documentation",
    version="1.0.0"
)

#Category = Enum("Category", ["ELECTRONICS", "CLOTHING", "FOOD", "OTHER"])
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


@app.post("/products", response_model=Product, status_code=201, tags=["products"])
async def create_product(product: Product):
    return product
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)