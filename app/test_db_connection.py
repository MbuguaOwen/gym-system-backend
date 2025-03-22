from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:11230428018@localhost/gym_db"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("✅ Database connection successful!")
except Exception as e:
    print("❌ Database connection failed:", e)
