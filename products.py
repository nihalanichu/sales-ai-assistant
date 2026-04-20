# this will have get_my_orders
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from security import get_current_user
from database import get_db
from models import Product
from schemas import CreateProduct

products_router = APIRouter(
    prefix="/api",
    tags=["products"]
)

@products_router.get("/products")
async def get_all_products(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    
    # fetch products from database and return list of products
    products = db.query(Product).all()
    return {"products": products}

# create new product, post API
@products_router.post("/products")
async def create_product(product: CreateProduct, current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    # title, category, price, description, current_stock
    new_product = Product(
        title=product.title,
        category=product.category,
        price=product.price,
        description=product.description,
        current_stock=product.current_stock
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product created successfully", "product": new_product}