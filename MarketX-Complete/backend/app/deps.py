from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .security import decode_token
bearer=HTTPBearer(auto_error=False)
def current_user(creds: HTTPAuthorizationCredentials=Depends(bearer), db: Session=Depends(get_db)):
    uid=decode_token(creds.credentials) if creds else None
    user=db.get(User,uid) if uid else None
    if not user: raise HTTPException(401,"Please sign in")
    return user
