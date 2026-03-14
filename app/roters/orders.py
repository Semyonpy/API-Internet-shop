from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import literal

from auth import get_db
from ..models import CartItem, Order, OrderItem
from ..schemas import OrderResponse, OrderItemResponse


def get_current_user():
    class User:
        id = 1

    return User()


router = APIRouter()


@router.post("/orders", response_model=OrderResponse)
def create_order(
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == literal(user.id)
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = Order(user_id=user.id)
    db.add(order)
    db.commit()
    db.refresh(order)

    order_items = []
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)
        order_items.append(order_item)
        db.delete(item)

    db.commit()

    # Присваиваем список items к order для Pydantic
    order.items = order_items

    return order