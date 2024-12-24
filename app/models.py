from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="guest")  # admin, manager, guest

    bookings = relationship("Booking", back_populates="owner")
    reviews = relationship("Review", back_populates="author")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)  # Numero della stanza
    type = Column(String)  # Tipo di stanza (es. "singola", "doppia", "suite")
    price_per_night = Column(Float)  # Prezzo per notte
    description = Column(String)  # Descrizione della stanza
    capacity = Column(Integer)  # Capacità della stanza
    available = Column(Boolean, default=True)  # Disponibilità

    bookings = relationship("Booking", back_populates="room")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Riferimento all'utente che ha effettuato la prenotazione
    room_id = Column(Integer, ForeignKey("rooms.id"))  # Riferimento alla stanza prenotata
    check_in_date = Column(Date)  # Data di check-in
    check_out_date = Column(Date)  # Data di check-out
    total_price = Column(Float)  # Prezzo totale della prenotazione
    status = Column(String, default="pending")  # Stato della prenotazione (es. "pending", "confirmed", "canceled")

    # Relazioni con gli altri modelli
    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)  # Una prenotazione ha un solo pagamento

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Riferimento all'utente che lascia la recensione
    room_id = Column(Integer, ForeignKey("rooms.id"))  # Riferimento alla stanza recensita
    rating = Column(Integer)  # Voto (ad esempio da 1 a 5)
    comment = Column(String)  # Commento della recensione
    created_at = Column(DateTime, default=datetime.utcnow)  # Data e ora di creazione della recensione

    # Relazioni con gli altri modelli
    user = relationship("User", back_populates="reviews")
    room = relationship("Room", back_populates="reviews")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))  # Riferimento alla prenotazione associata
    amount = Column(Float)  # Importo pagato
    payment_date = Column(DateTime, default=datetime.utcnow)  # Data e ora del pagamento
    payment_method = Column(String)  # Metodo di pagamento (es. "carta di credito", "PayPal")
    status = Column(String, default="completed")  # Stato del pagamento (es. "completed", "pending", "failed")

    # Relazione con il modello Booking
    booking = relationship("Booking", back_populates="payment")