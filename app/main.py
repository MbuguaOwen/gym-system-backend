import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal  # Import SessionLocal
from db_models import Member  # Import Member model
from fastapi.routing import APIRoute

app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Gym System API"}

# Dependency to get a new database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provides the session
    finally:
        db.close()  # Closes the session after request

# API Route to create a new gym member
@app.post("/members/")
def create_member(name: str, email: str, phone_number: str, db: Session = Depends(get_db)):
    new_member = Member(name=name, email=email, phone_number=phone_number, membership_end="2025-12-31")
    db.add(new_member)  # Add to database
    db.commit()  # Save changes
    db.refresh(new_member)  # Refresh the object
    return {"message": "Member added!", "member": new_member}

# API Route to retrieve all members
@app.get("/members")
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

# Print all registered routes
for route in app.router.routes:
    print(f"Path: {route.path}, Methods: {route.methods}")