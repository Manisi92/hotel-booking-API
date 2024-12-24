from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# Schemi per User
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True

# Schemi per Room
class RoomBase(BaseModel):
    number: str
    type: str
    price_per_night: float
    description: Optional[str] = None
    capacity: int
    available: bool = True

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True

# Schemi per Booking
class BookingBase(BaseModel):
    user_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    total_price: float
    status: str = "pending"

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True

# Schemi per Review
class ReviewBase(BaseModel):
    user_id: int
    room_id: int
    rating: int
    comment: Optional[str] = None
    created_at: Optional[date] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True

# Schemi per Payment
class PaymentBase(BaseModel):
    booking_id: int
    amount: float
    payment_date: date
    payment_method: str
    status: str = "completed"

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int

    class Config:
        orm_mode = True
