from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.routers.auth_router import get_current_admin

router = APIRouter(prefix="/products", tags=["Products"])

# 🔐 Create Product (Admin only)
@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Get All Products (Public)
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# Get Single Product (Public)
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 🔐 Update Product (Admin only)
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated_data: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated_data.name
    product.description = updated_data.description
    product.price = updated_data.price
    product.stock = updated_data.stock

    db.commit()
    db.refresh(product)
    return product

# 🔐 Delete Product (Admin only)
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}