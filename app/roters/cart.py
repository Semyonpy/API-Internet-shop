from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .auth import get_db
from ..models import CartItem, Product
from ..schemas import CartCreate, CartResponse

router = APIRouter()


# Заглушка
def get_current_user():
    class User:
        id = 1  #тестовый пользователь

    return User()


@router.post("/cart", response_model=CartResponse)
def add_to_cart(
        item: CartCreate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    product_id = int(item.product_id)
    user_id = int(user.id)
    # Проверяем, есть ли продукт
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Проверяем, есть ли продукт уже в корзине
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity  # увеличиваем количество
    else:
        cart_item = CartItem(
            user_id=user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)  # обновляем объект после коммита

    return cart_item