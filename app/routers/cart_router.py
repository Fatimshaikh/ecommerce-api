from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.cart_model import CartItem
from app.models.product_model import Product
from app.schemas.cart_schema import CartItemCreate, CartItemResponse
from app.routers.auth_router import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

# Add item to cart
@router.post("/", response_model=CartItemResponse)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = db.query(CartItem).filter(
        CartItem.user_id == user.id, CartItem.product_id == item.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(
            user_id=user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return CartItemResponse(
        id=cart_item.id,
        product_id=product.id,
        product_name=product.name,
        quantity=cart_item.quantity,
        price=product.price
    )

# Get all items in user's cart
@router.get("/", response_model=list[CartItemResponse])
def get_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    response = []
    for item in cart_items:
        response.append(
            CartItemResponse(
                id=item.id,
                product_id=item.product.id,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price
            )
        )
    return response

# Update quantity
@router.put("/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(cart_item_id: int, quantity: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id, CartItem.user_id == user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)

    return CartItemResponse(
        id=cart_item.id,
        product_id=cart_item.product.id,
        product_name=cart_item.product.name,
        quantity=cart_item.quantity,
        price=cart_item.product.price
    )

# Delete cart item
@router.delete("/{cart_item_id}")
def delete_cart_item(cart_item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id, CartItem.user_id == user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Cart item removed"}