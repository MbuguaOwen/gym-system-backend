import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Adds current directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Adds backend

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

from app.database import SessionLocal, engine, Base
from app.db_models import Admin, Member

from fastapi.middleware.cors import CORSMiddleware
import secrets

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
    email: EmailStr
    phone: str
    membership_start: datetime = None
    membership_end: datetime = None

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

    membership_start = member_data.membership_start or datetime.utcnow()
    membership_end = member_data.membership_end or (membership_start + timedelta(days=30))

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
        "membership_start": new_member.membership_start.isoformat(),
        "membership_end": new_member.membership_end.isoformat()
    }}

# ✅ Get All Members
@app.get("/members")
def get_members(db: Session = Depends(get_db)):
    members = db.query(Member).all()

    active_members = [m for m in members if m.membership_end > datetime.utcnow()]
    expired_members = [m for m in members if m.membership_end <= datetime.utcnow()]

    active_members.sort(key=lambda m: m.membership_end)
    expired_members.sort(key=lambda m: m.membership_end)

    sorted_members = active_members + expired_members

    return [{
        "id": m.id,
        "name": m.name,
        "email": m.email,
        "phone": m.phone_number,
        "membership_start": m.membership_start.isoformat(),
        "membership_end": m.membership_end.isoformat()
    } for m in sorted_members]

# ✅ Update Member
@app.put("/members/{member_id}")
def update_member(member_id: int, member_data: MemberSchema, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    member.name = member_data.name
    member.email = member_data.email
    member.phone_number = member_data.phone
    member.membership_start = member_data.membership_start or member.membership_start
    member.membership_end = member_data.membership_end or (member.membership_start + timedelta(days=30))

    db.commit()
    db.refresh(member)
    return {"message": "Member updated successfully", "member": {
        "id": member.id,
        "name": member.name,
        "email": member.email,
        "phone": member.phone_number,
        "membership_start": member.membership_start.isoformat(),
        "membership_end": member.membership_end.isoformat()
    }}

# ✅ Delete Member
@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(member)
    db.commit()
    return {"message": "Member deleted successfully"}
