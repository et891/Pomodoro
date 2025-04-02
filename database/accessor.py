from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/pomodoro")
SessionLocal = sessionmaker(bind=engine)  # 👈 лучше назвать SessionLocal по стандарту

def get_db_session() -> Session:
    return SessionLocal()
