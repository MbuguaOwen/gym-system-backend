from datetime import datetime
from database import SessionLocal
from sqlalchemy.orm import Session
from db_models import Member  # Assuming you have a Member model

def deactivate_expired_members():
    session: Session = SessionLocal()

    try:
        today = datetime.now()
        expired_members = (
            session.query(Member)
            .filter(Member.membership_end < today, Member.is_active == True)
            .all()
        )

        for member in expired_members:
            member.is_active = False

        session.commit()
        print(f"✅ {len(expired_members)} expired memberships deactivated!")
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    deactivate_expired_members()
