from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine  # ✅ Load database first
from app.db_models import Member, Base

from fastapi.middleware.cors import CORSMiddleware
from app.expiry_date import calculate_expiry
from datetime import datetime

start_date = datetime.today()
expiry_date = calculate_expiry(start_date, "yearly")
print("Membership expires on:", expiry_date)

# Initialize FastAPI app
app = FastAPI()

# Ensure database tables are created
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⛔️ This allows all origins (for dev). Change to your frontend URL in production.
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # ✅ Allow all headers
)
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
    db.commit()  # ✅ Ensure changes are saved
    db.refresh(new_member)
    
        # ✅ Return all members to check if it was added
    members = db.query(Member).all()
    return {"message": "Member added!", "all_members": members}

# API Route to retrieve all members
@app.get("/members")
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

