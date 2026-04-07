from pydantic import BaseModel

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: float

    class Config:
        orm_mode = True