import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Adds current directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Adds backend

print("Updated PYTHONPATH:", sys.path)  # Debugging

from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.database import SessionLocal, engine, Base
from app.db_models import Admin, Member

from fastapi.middleware.cors import CORSMiddleware

import secrets
print(secrets.token_hex(32))


DEBUG = os.getenv("DEBUG", "False") == "True"

if DEBUG:
    print("Running in DEBUG mode!")

# Initialize FastAPI app
app = FastAPI()

# Ensure database tables are created
Base.metadata.create_all(bind=engine)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# OAuth2 security setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin-access")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Admin Schema
class AdminSchema(BaseModel):
    email: EmailStr
    password: str

# ✅ Member Schema
class MemberSchema(BaseModel):
    name: str
    email: EmailStr  # Ensures valid email format
    phone: str
    membership_start: datetime = None  # Optional, defaults to current time
    membership_end: datetime = None  # Optional, defaults to 30 days from now

# ✅ Admin Signup/Login (Returns Token)
@app.post("/admin-access")
def admin_access(admin_data: AdminSchema, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == admin_data.email).first()

    if not admin:
        new_admin = Admin(email=admin_data.email, password_hash=hash_password(admin_data.password))
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return {"message": "Admin created successfully!", "token": "fake-jwt-token"}

    if not verify_password(admin_data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "token": "fake-jwt-token"}

# ✅ Add New Member
@app.post("/members")
def add_member(member_data: MemberSchema, db: Session = Depends(get_db)):
    existing_member = db.query(Member).filter(Member.phone_number == member_data.phone).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="Phone number already exists. Use a different number.")
    
    membership_start = datetime.utcnow()
    membership_end = datetime.utcnow() + timedelta(days=30)  # Default 30 days
    new_member = Member(
        name=member_data.name,
        email=member_data.email,
        phone_number=member_data.phone,
        membership_start=membership_start,
        membership_end=membership_end,
        is_active=True
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return {"message": "Member added successfully!", "member": {
        "id": new_member.id,
        "name": new_member.name,
        "email": new_member.email,
        "phone": new_member.phone_number,
        "membership_start": new_member.membership_start.isoformat(),  # Ensure ISO format
        "membership_end": new_member.membership_end.isoformat()  # Ensure ISO format
    }}

# ✅ Get All Members (No Auth for Now)
@app.get("/members")
def get_members(db: Session = Depends(get_db)):
    # Query members from the database
    members = db.query(Member).all()

    # Separate members into active and expired based on membership_end
    active_members = [m for m in members if m.membership_end > datetime.utcnow()]
    expired_members = [m for m in members if m.membership_end <= datetime.utcnow()]

    # Sort active members by membership_end date (ascending)
    active_members.sort(key=lambda m: m.membership_end)

    # Sort expired members by membership_end date (ascending)
    expired_members.sort(key=lambda m: m.membership_end)

    # Combine active and expired members into one list (active first)
    sorted_members = active_members + expired_members

    # Return members with the sorted list
    return [{"id": m.id, "name": m.name, "email": m.email, "phone": m.phone_number, 
             "membership_start": m.membership_start.isoformat(), 
             "membership_end": m.membership_end.isoformat()} 
            for m in sorted_members]

# ✅ Delete Member
@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(member)
    db.commit()
    return {"message": "Member deleted successfully"}
