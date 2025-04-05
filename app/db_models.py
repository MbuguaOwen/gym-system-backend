from app.database import Base  # ✅ Correct import
from sqlalchemy import Column, Integer, String, Date, Boolean
import datetime


# Define the Member model
class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True)
    fingerprint_id = Column(String, unique=True, nullable=True)  # To be added later
    membership_start = Column(Date, default=datetime.date.today)
    membership_end = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

# Define the Admin model
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
