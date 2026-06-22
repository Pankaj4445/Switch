
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from config import SessionLocal, engine
import databaseModels
from sqlalchemy.orm import Session
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware
databaseModels.Base.metadata.create_all(engine)
@app.get("/")
async def root():
    return {"message": "Hello World"}

allproducts = [
    Product(id=1, name="Mobile", price=10.99, description="Mobile phone with 4GB RAM and 64GB storage"),
    Product(id=2, name="Tv", price=19.99, description="Smart TV with 4K resolution and HDR support"),
    Product(id=3, name="Laptop", price=5.99, description="Laptop with 8GB RAM and 256GB SSD"),
    Product(id=4, name="Headphones", price=15.99, description="Wireless headphones with noise cancellation"),
    Product(id=5, name="Camera", price=25.99, description="Digital camera with 20MP sensor"),]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = SessionLocal()

    count = db.query(databaseModels.Product).count()
    if count == 0:
        for product in allproducts:
            db_product = databaseModels.Product(id=product.id, name=product.name, price=product.price, description=product.description)
            db.add(db_product)
        db.commit()
        db.close()
init_db()


@app.get('/products')
async def get_products(db: Session = Depends(get_db)):
    dbproducts = db.query(databaseModels.Product).all()
    return dbproducts

@app.get('/products/{product_id}')
async def get_product(product_id: int, db: Session = Depends(get_db)):
    dbproduct = db.query(databaseModels.Product).filter(databaseModels.Product.id == product_id).first()
    if dbproduct:
        return dbproduct
    return {"error": "Product not found"}


@app.post('/products')
async def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(databaseModels.Product(**product.model_dump()))
    db.commit()
    return product

@app.put('/products/{product_id}')
async def update_product(product_id: int, update_product:Product, db: Session = Depends(get_db)):
    dbproduct = db.query(databaseModels.Product).filter(databaseModels.Product.id == product_id).first()
    if dbproduct:
        dbproduct.name = update_product.name
        dbproduct.price = update_product.price
        dbproduct.description = update_product.description
        db.commit()
        return dbproduct
    return {"error": "Product not found"}


@app.delete('/products/{product_id}')
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    dbproduct = db.query(databaseModels.Product).filter(databaseModels.Product.id == product_id).first()
    if dbproduct:
        db.delete(dbproduct)
        db.commit()
        return {"message": "Product deleted", "products": allproducts}
    return {"error": "Product not found"}
    