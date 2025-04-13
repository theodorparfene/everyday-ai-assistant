from sqlalchemy import create_engine

# root:password (in this case password is just root, too lazy to think of another one)
MYSQL_URL = "mysql+pymysql://root:root@localhost:3306/ai_assistant"

engine = create_engine(MYSQL_URL)

try:
    with engine.connect() as conn:
        print("✅ Connected to MySQL as root!")
except Exception as e:
    print("❌ Failed to connect:", e)