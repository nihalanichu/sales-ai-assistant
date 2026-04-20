from pydantic import BaseModel, EmailStr

# full_name, email, password
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# create CreateProduct model with title, category, price, description, current_stock
class CreateProduct(BaseModel):
    title: str
    category: str
    price: int
    description: str
    current_stock: int

