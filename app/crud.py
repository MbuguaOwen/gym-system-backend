from sqlalchemy.orm import Session
from . import db_models  # Assuming the models are in db_models.py
from datetime import datetime


# Create a new member
def create_member(db: Session, name: str, email: str, phone_number: str, membership_start: datetime, membership_end: datetime):
    db_member = db_models.Member(
        name=name,
        email=email,
        phone_number=phone_number,
        membership_start=membership_start,
        membership_end=membership_end,
        is_active=True
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


# Get all members
def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Member).offset(skip).limit(limit).all()


# Get member by ID
def get_member(db: Session, member_id: int):
    return db.query(db_models.Member).filter(db_models.Member.id == member_id).first()


# Update member details (including membership dates)
def update_member(db: Session, member_id: int, name: str, email: str, phone_number: str, membership_start: datetime, membership_end: datetime):
    db_member = db.query(db_models.Member).filter(db_models.Member.id == member_id).first()
    if db_member:
        db_member.name = name
        db_member.email = email
        db_member.phone_number = phone_number
        db_member.membership_start = membership_start
        db_member.membership_end = membership_end
        db.commit()
        db.refresh(db_member)
        return db_member
    return None


# Delete member
def delete_member(db: Session, member_id: int):
    db_member = db.query(db_models.Member).filter(db_models.Member.id == member_id).first()
    if db_member:
        db.delete(db_member)
        db.commit()
        return db_member
    return None
