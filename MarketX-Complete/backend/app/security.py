from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from .config import settings
pwd=CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM="HS256"
def hash_password(password): return pwd.hash(password)
def verify_password(password, hashed): return pwd.verify(password, hashed)
def create_token(user_id):
    exp=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub":str(user_id),"exp":exp},settings.SECRET_KEY,algorithm=ALGORITHM)
def decode_token(token):
    try: return int(jwt.decode(token,settings.SECRET_KEY,algorithms=[ALGORITHM])["sub"])
    except (JWTError, ValueError, KeyError): return None
