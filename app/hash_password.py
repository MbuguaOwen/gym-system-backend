from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "admin"  # Change this if needed
hashed_password = pwd_context.hash(password)

print(f"Hashed password for '{password}': {hashed_password}")
