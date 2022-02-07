from passlib.context import CryptContext #pip install passlib[bcrypt]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function for hashing our password (hashing is in one direction)
def hash(password: str):
    return pwd_context.hash(password)



# Function for hashing the login password and conpare it with the password hashed in the database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


