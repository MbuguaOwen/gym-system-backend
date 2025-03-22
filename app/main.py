from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine  # ✅ Load database first
from app.db_models import Member, Base
from app.schemas import MemberCreate, MemberResponse  # ✅ Import schemas
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

# ✅ Corrected Swagger UI Post Request
@app.post("/members/", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    new_member = Member(
        name=member.name,
        email=member.email,
        phone_number=member.phone_number,
        membership_end=member.membership_end or "2025-12-31"
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    return new_member  # ✅ Now returns correct response format

# API Route to retrieve all members
@app.get("/members")
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

