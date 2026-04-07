from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.order_model import Order, OrderItem
from app.models.cart_model import CartItem
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderItemResponse
from app.routers.auth_router import get_current_user, get_current_admin

router = APIRouter(prefix="/orders", tags=["Orders"])

# Place an order from cart
@router.post("/", response_model=OrderResponse)
def place_order(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = sum(item.quantity * item.product.price for item in cart_items)

    order = Order(user_id=user.id, total_price=total_price)
    db.add(order)
    db.commit()
    db.refresh(order)

    order_items_res = []
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.add(order_item)
        order_items_res.append(
            OrderItemResponse(
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price
            )
        )
        db.delete(item)  # Clear item from cart

    db.commit()

    return OrderResponse(
        id=order.id,
        user_id=user.id,
        items=order_items_res,
        total_price=total_price
    )

# Get current user's orders
@router.get("/", response_model=list[OrderResponse])
def get_my_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    response = []
    for order in orders:
        items = [
            OrderItemResponse(
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.price
            )
            for item in order.order_items
        ]
        response.append(OrderResponse(
            id=order.id,
            user_id=user.id,
            items=items,
            total_price=order.total_price
        ))
    return response

# Admin: get all orders
@router.get("/all")
def get_all_orders(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    orders = db.query(Order).all()
    response = []
    for order in orders:
        items = [
            OrderItemResponse(
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.price
            )
            for item in order.order_items
        ]
        response.append(OrderResponse(
            id=order.id,
            user_id=order.user_id,
            items=items,
            total_price=order.total_price
        ))
    return response