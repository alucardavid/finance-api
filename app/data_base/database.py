from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "postgresql://postgres.yuduhfwulcdmflcsinwp:DevGenius%40123@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
