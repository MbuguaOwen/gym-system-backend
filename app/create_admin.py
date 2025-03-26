
import sys
import os

# Add the backend directory to Python's path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from sqlalchemy.orm import Session
from database import SessionLocal
from db_models import Admin

def create_admin():
    db: Session = SessionLocal()

    # Create an admin user with a plain password
    new_admin = Admin(email="admin@gmail.com", password_hash="admin")  # 🚨 Storing password in plain text
    db.add(new_admin)
    db.commit()
    db.close()

    print("✅ Admin created successfully!")

if __name__ == "__main__":
    create_admin()
