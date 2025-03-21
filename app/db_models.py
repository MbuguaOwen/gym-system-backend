from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Database connection URL - Update with your actual PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:11230428018@localhost/gym_db"

# Create database engine
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

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

# Create tables in the database
if __name__ == "__main__":
    print("🚀 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
