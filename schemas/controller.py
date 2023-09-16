from typing import Optional,List
from pydantic import BaseModel


class UserInput(BaseModel):
    name: str
    email: str
    phone_number: str

class UserCount(BaseModel):
    total: int

class RestaurantInput(BaseModel):
    name: str
    location: str

class FoodInput(BaseModel):
    name: str
    price: int
    description: str
    restaurant_id: int

class FoodDelete(BaseModel):
    food_id: int
    restaurant_id: int

class TicketPurchaseInput(BaseModel):
    customer_id: int
    validation_status: str

class BookingCreateInput(BaseModel):
    customer_id: int
    restaurant_id: int

class BookingGetListInput(BaseModel):
    customer_id: int

class BookingUpdateInput(BaseModel):
    status: str

# Model untuk mewakili detail makanan yang dipesan
class FoodOrder(BaseModel):
    food_id: int
    quantity: int

class BookingCreateInput(BaseModel):
    customer_id: int
    restaurant_id: int
    foods: List[FoodOrder]  # Menyimpan daftar makanan yang dipesan