from .database import Base,engine,SessionLocal
from .models import User,Listing
from .security import hash_password
Base.metadata.create_all(bind=engine)
db=SessionLocal()
try:
    users={}
    for email,name,phone in [("demo@marketx.in","MarketX Demo","9876543210"),("seller@marketx.in","Aarav Sharma","9123456780")]:
        u=db.query(User).filter_by(email=email).first()
        if not u:
            u=User(email=email,name=name,phone=phone,password_hash=hash_password("MarketX@123")); db.add(u); db.flush()
        users[email]=u
    samples=[
      ("iPhone 13 128GB","Excellent condition, battery health 88%. Box and cable included.",28500,"Mobiles","Used","Hyderabad","Telangana","https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=900"),
      ("Modern 3-seater sofa","Comfortable premium fabric sofa, gently used and well maintained.",14500,"Furniture","Used","Serilingampalle","Telangana","https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=900"),
      ("Honda City 2020","Single owner, full service history, smooth drive.",725000,"Cars","Used","Hyderabad","Telangana","https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=900"),
      ("Gaming laptop","16GB RAM, 512GB SSD, dedicated graphics. Great for gaming and work.",62000,"Electronics","Used","Bengaluru","Karnataka","https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=900"),
      ("Road bicycle","Lightweight frame, recently serviced, ready to ride.",9500,"Bikes","Used","Pune","Maharashtra","https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=900"),
      ("2BHK apartment for rent","Bright apartment with balcony, parking and 24-hour water.",22000,"Properties","Rent","Hyderabad","Telangana","https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=900")
    ]
    if db.query(Listing).count()==0:
        for i,s in enumerate(samples): db.add(Listing(title=s[0],description=s[1],price=s[2],category=s[3],condition=s[4],city=s[5],state=s[6],image_url=s[7],seller_id=users["seller@marketx.in"].id))
    db.commit()
    print("Seed complete. Demo password: MarketX@123")
finally: db.close()
