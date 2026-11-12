import os, uuid
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from .database import Base, engine, get_db
from .models import User, Listing, Favorite
from .schemas import RegisterIn, LoginIn, UserOut, TokenOut, ListingIn, ListingUpdate, ListingOut
from .security import hash_password, verify_password, create_token
from .deps import current_user
from .config import settings

Base.metadata.create_all(bind=engine)
os.makedirs("uploads",exist_ok=True)
app=FastAPI(title="MarketX API", version="1.0.0", description="Buy Nearby. Sell Everywhere.")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.CORS_ORIGINS.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")

@app.get("/api/health")
def health(): return {"status":"ok","service":"MarketX API"}

@app.post("/api/auth/register",response_model=TokenOut,status_code=201)
def register(data:RegisterIn,db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==data.email.lower()).first(): raise HTTPException(409,"Email already registered")
    user=User(name=data.name.strip(),email=data.email.lower(),phone=data.phone,password_hash=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token":create_token(user.id),"user":user}

@app.post("/api/auth/login",response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==data.email.lower()).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Invalid email or password")
    return {"access_token":create_token(user.id),"user":user}

@app.get("/api/auth/me",response_model=UserOut)
def me(user:User=Depends(current_user)): return user

@app.get("/api/categories")
def categories():
    return ["Mobiles","Electronics","Cars","Bikes","Properties","Furniture","Fashion","Pets","Books & Sports","Services","Home Appliances","Agriculture"]

@app.get("/api/listings",response_model=list[ListingOut])
def get_listings(q:str="",category:str="",city:str="",state:str="",sort:str="newest",limit:int=Query(60,ge=1,le=100),offset:int=0,db:Session=Depends(get_db)):
    query=db.query(Listing).options(joinedload(Listing.seller)).filter(Listing.is_active==True)
    if q: query=query.filter(or_(Listing.title.ilike(f"%{q}%"),Listing.description.ilike(f"%{q}%")))
    if category: query=query.filter(Listing.category==category)
    if city: query=query.filter(Listing.city.ilike(f"%{city}%"))
    if state: query=query.filter(Listing.state.ilike(f"%{state}%"))
    query=query.order_by(Listing.price.asc() if sort=="price_low" else Listing.price.desc() if sort=="price_high" else Listing.created_at.desc())
    return query.offset(offset).limit(limit).all()

@app.get("/api/listings/{listing_id}",response_model=ListingOut)
def get_listing(listing_id:int,db:Session=Depends(get_db)):
    item=db.query(Listing).options(joinedload(Listing.seller)).filter(Listing.id==listing_id,Listing.is_active==True).first()
    if not item: raise HTTPException(404,"Listing not found")
    return item

@app.post("/api/listings",response_model=ListingOut,status_code=201)
def create_listing(data:ListingIn,db:Session=Depends(get_db),user:User=Depends(current_user)):
    item=Listing(**data.model_dump(),seller_id=user.id); db.add(item); db.commit()
    return db.query(Listing).options(joinedload(Listing.seller)).get(item.id)

@app.patch("/api/listings/{listing_id}",response_model=ListingOut)
def update_listing(listing_id:int,data:ListingUpdate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    item=db.get(Listing,listing_id)
    if not item: raise HTTPException(404,"Listing not found")
    if item.seller_id!=user.id: raise HTTPException(403,"You can only edit your own ads")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(item,k,v)
    db.commit(); return db.query(Listing).options(joinedload(Listing.seller)).get(item.id)

@app.delete("/api/listings/{listing_id}")
def delete_listing(listing_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    item=db.get(Listing,listing_id)
    if not item: raise HTTPException(404,"Listing not found")
    if item.seller_id!=user.id: raise HTTPException(403,"You can only delete your own ads")
    item.is_active=False; db.commit(); return {"message":"Listing removed"}

@app.post("/api/listings/{listing_id}/favorite")
def toggle_favorite(listing_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    if not db.get(Listing,listing_id): raise HTTPException(404,"Listing not found")
    fav=db.query(Favorite).filter_by(user_id=user.id,listing_id=listing_id).first()
    if fav: db.delete(fav); saved=False
    else: db.add(Favorite(user_id=user.id,listing_id=listing_id)); saved=True
    db.commit(); return {"saved":saved}

@app.get("/api/favorites",response_model=list[ListingOut])
def favorites(db:Session=Depends(get_db),user:User=Depends(current_user)):
    return db.query(Listing).join(Favorite,Favorite.listing_id==Listing.id).options(joinedload(Listing.seller)).filter(Favorite.user_id==user.id,Listing.is_active==True).all()

@app.post("/api/upload")
async def upload_image(file:UploadFile=File(...),user:User=Depends(current_user)):
    ext=os.path.splitext(file.filename or "")[1].lower()
    if ext not in {".jpg",".jpeg",".png",".webp"}: raise HTTPException(400,"Only JPG, PNG and WEBP images are allowed")
    data=await file.read()
    if len(data)>5*1024*1024: raise HTTPException(413,"Image must be 5 MB or smaller")
    name=f"{uuid.uuid4().hex}{ext}"
    with open(os.path.join("uploads",name),"wb") as f: f.write(data)
    return {"image_url":f"/uploads/{name}"}
