from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

env_file_path = os.getcwd()+"\\src\\.env"
load_dotenv(dotenv_path=env_file_path)

# Connect to Supabase via connection pooling with Supavisor.
# DATABASE_URL="postgresql://postgres.itwetgwiwyimperdatby:Shivtej28@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true"

# Direct connection to the database. Used for migrations.Shivtejdeshmukh
DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "postgresql://postgres.itwetgwiwyimperdatby:Shivtej28@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
# DATABASE_URL = "sqlite:///./money_manager.db"
# DATABASE_URL = "https://itwetgwiwyimperdatby.supabase.co/storage/v1/object/public/Money%20Manager//money_manager.db"
print("-------------------------------------------------------------" + DATABASE_URL)

# F:\Personal Projects\Money Manager\money-manager-api\money-manager-api\src\.env
# F:\Personal Projects\Money Manager\money-manager-api\money-manager-api\src\.env


# "postgresql://myuser:UlyQEliEJAJbqgttFRDo9KTKWbUhLwZN@dpg-crq2i0l6l47c73askj5g-a.oregon-postgres.render.com/moneymanagerdb_4d4y"
# DATABASE_URL = "postgresql://myuser:mypassword@localhost/moneymanagerdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
