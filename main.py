from db import engine
from models import Base

Base.metadata.create_all(bind=engine)
print("✅ Knowledge base table created.")