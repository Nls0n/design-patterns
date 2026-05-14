import time
from .database import engine, Base, SessionLocal
from .models import OrderModel
from sqlalchemy.exc import OperationalError

def seed():
    max_retries = 10
    for _ in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            db = SessionLocal()
            if db.query(OrderModel).count() == 0:
                for i in range(1, 25):
                    order = OrderModel(
                        customer_name=f"Customer_{i}", 
                        total_price=10.0 + i, 
                        status="Pending"
                    )
                    db.add(order)
                db.commit()
            db.close()
            break
        except OperationalError:
            time.sleep(2)

if __name__ == "__main__":
    seed()