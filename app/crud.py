from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# --------- User CRUD ---------
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --------- Room CRUD ---------
def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(
        number=room.number,
        type=room.type,
        price_per_night=room.price_per_night,
        description=room.description,
        capacity=room.capacity,
        available=room.available
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def get_rooms(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Room).offset(skip).limit(limit).all()

def update_room(db: Session, room_id: int, room: schemas.RoomCreate):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room:
        db_room.number = room.number
        db_room.type = room.type
        db_room.price_per_night = room.price_per_night
        db_room.description = room.description
        db_room.capacity = room.capacity
        db_room.available = room.available
        db.commit()
        db.refresh(db_room)
    return db_room

def delete_room(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room:
        db.delete(db_room)
        db.commit()
    return db_room

# --------- Booking CRUD ---------
def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        total_price=booking.total_price,
        status=booking.status
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_bookings_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).offset(skip).limit(limit).all()

def get_bookings_by_room(db: Session, room_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Booking).filter(models.Booking.room_id == room_id).offset(skip).limit(limit).all()

def update_booking(db: Session, booking_id: int, booking: schemas.BookingCreate):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking:
        db_booking.user_id = booking.user_id
        db_booking.room_id = booking.room_id
        db_booking.check_in_date = booking.check_in_date
        db_booking.check_out_date = booking.check_out_date
        db_booking.total_price = booking.total_price
        db_booking.status = booking.status
        db.commit()
        db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
    return db_booking

# --------- Review CRUD ---------
def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(
        user_id=review.user_id,
        room_id=review.room_id,
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at or datetime.utcnow()
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def get_reviews_by_room(db: Session, room_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Review).filter(models.Review.room_id == room_id).offset(skip).limit(limit).all()

def get_reviews_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Review).filter(models.Review.user_id == user_id).offset(skip).limit(limit).all()

def delete_review(db: Session, review_id: int):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review

# --------- Payment CRUD ---------
def create_payment(db: Session, payment: schemas.PaymentCreate):
    db_payment = models.Payment(
        booking_id=payment.booking_id,
        amount=payment.amount,
        payment_date=payment.payment_date,
        payment_method=payment.payment_method,
        status=payment.status
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()

def get_payments_by_booking(db: Session, booking_id: int):
    return db.query(models.Payment).filter(models.Payment.booking_id == booking_id).all()

def update_payment(db: Session, payment_id: int, payment: schemas.PaymentCreate):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment:
        db_payment.amount = payment.amount
        db_payment.payment_date = payment.payment_date
        db_payment.payment_method = payment.payment_method
        db_payment.status = payment.status
        db.commit()
        db.refresh(db_payment)
    return db_payment

def delete_payment(db: Session, payment_id: int):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment:
        db.delete(db_payment)
        db.commit()
    return db_payment
