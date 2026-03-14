from fastapi import FastAPI
from database import Base, engine
from roters import auth, products, cart, orders

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)