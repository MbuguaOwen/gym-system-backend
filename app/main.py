from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.db_models import Member, Base  # Import models

# Initialize FastAPI app
app = FastAPI()

# Ensure database tables are created
Base.metadata.create_all(bind=engine)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Gym System API"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "Backend is running!"}

# Dependency to get a new database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Route to create a new gym member
@app.post("/members/")
def create_member(name: str, email: str, phone_number: str, db: Session = Depends(get_db)):
    new_member = Member(name=name, email=email, phone_number=phone_number, membership_end="2025-12-31")
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return {"message": "Member added!", "member": new_member}

# API Route to retrieve all members
@app.get("/members")
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()
