from passlib.context import CryptContext #pip install passlib[bcrypt]
import random, string
import boto3
from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function for hashing our password (hashing is in one direction)
def hash(password: str):
    return pwd_context.hash(password)


# Function for hashing the login password and conpare it with the password hashed in the database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



# Create the new name
def create_new_name(filename):
    extra = "".join([random.choice(string.ascii_uppercase) for _ in range(20)])
    return f'{extra}{filename}'


# Upload file to aws s3 with boto3
def upload_file(filename):
    # Creating Session With Boto3.
    session = boto3.Session(aws_access_key_id=settings.aws_access_key_id,aws_secret_access_key=settings.aws_secret_access_key)
    # Creating S3 Resource From the Session.
    s3 = session.resource('s3')

    result = s3.Bucket(settings.aws_bucket_name).upload_file(f'media/images/{filename}', f'new/{filename}')
    print(result)
    path = f'https://est-fbs-blogs-bucket.s3.us-east-2.amazonaws.com/new/{filename}'
    return path
