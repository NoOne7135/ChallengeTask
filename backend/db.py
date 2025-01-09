from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./bets.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    pool_size=20,
    max_overflow=40,
    pool_timeout=30 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer)
    type = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
