from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

env_file_path = os.getcwd()+"\\src\\.env"
load_dotenv(dotenv_path=env_file_path)

#DATABASE_URL="postgresql://shivtej:Shivtej28@money-manager-database.cetmy26qsy18.us-east-1.rds.amazonaws.com:5432/moneymanager"
DATABASE_URL = "sqlite:///./money_manager.db"
#DATABASE_URL = "mssql+pyodbc://Server=DESKTOP-D1MLGPR\SQLEXPRESS;Database=master;Trusted_Connection=True;driver=ODBC+Driver+17+for+SQL+Server;Trusted_Connection=True;"
print("-------------------------------------------------------------"+ DATABASE_URL)

# F:\Personal Projects\Money Manager\money-manager-api\money-manager-api\src\.env
# F:\Personal Projects\Money Manager\money-manager-api\money-manager-api\src\.env


#"postgresql://myuser:UlyQEliEJAJbqgttFRDo9KTKWbUhLwZN@dpg-crq2i0l6l47c73askj5g-a.oregon-postgres.render.com/moneymanagerdb_4d4y"
#DATABASE_URL = "postgresql://myuser:mypassword@localhost/moneymanagerdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()