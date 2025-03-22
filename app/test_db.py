from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db_models import Member  # Import the model

DATABASE_URL = "postgresql://postgres:11230428018@localhost/gym_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

# Check if there are any members
members = db.query(Member).all()
print("🔎 Members in DB:", members)

db.close()
