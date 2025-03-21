from database import Base  # Import Base from database.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
import datetime 


# Define the Member model
class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True)
    fingerprint_id = Column(String, unique=True, nullable=True)  # To be added later
    membership_start = Column(DateTime, default=datetime.datetime.utcnow)
    membership_end = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

# Define the Admin model
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
