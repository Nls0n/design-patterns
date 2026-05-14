from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .models import OrderModel
from .patterns import (
    DiscountPricing, CheeseDecorator, BasePizza, PaymentAdapter, LegacyPayment,
    AppProxy, MenuCategory, MenuItem, a_star
)

app = FastAPI()
Base.metadata.create_all(bind=engine)
proxy = AppProxy()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return proxy.render(access=True)

@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(OrderModel).all()

@app.get("/patterns/strategy")
def demo_strategy():
    strategy = DiscountPricing()
    return {"discounted_price": strategy.calculate(100.0)}

@app.get("/patterns/decorator")
def demo_decorator():
    pizza = CheeseDecorator(BasePizza())
    return {"total_pizza_cost": pizza.cost()}

@app.get("/patterns/adapter")
def demo_adapter():
    adapter = PaymentAdapter(LegacyPayment())
    return {"payment_success": adapter.pay(15.50)}

@app.get("/patterns/composite_iterator")
def demo_composite():
    menu = MenuCategory("Main Menu")
    menu.add(MenuItem("Pizza Margarita"))
    menu.add(MenuItem("Pizza Pepperoni"))
    items = [item.get_name() for item in menu]
    return {"menu_items": items}

@app.get("/patterns/math")
def demo_math():
    graph = {'A': {'B': 1, 'C': 4}, 'B': {'C': 2, 'D': 5}, 'C': {'D': 1}, 'D': {}}
    h = {'A': 3, 'B': 2, 'C': 1, 'D': 0}
    path = a_star(graph, 'A', 'D', h)
    return {"delivery_shortest_path": path}