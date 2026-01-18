from db import engine, Base
from models import User, Item

print("Connecting to Cloud SQL and creating tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Success! Tables 'users' and 'items' created in Cloud SQL.")
except Exception as e:
    print(f"❌ Error: {e}")