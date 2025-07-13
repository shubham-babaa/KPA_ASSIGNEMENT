from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Generator
from urllib.parse import quote_plus
import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        self.db_user = os.getenv("POSTGRES_USER", "admin")
        self.db_pass = quote_plus(os.getenv("POSTGRES_PASSWORD", "baba@321"))
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_name = os.getenv("POSTGRES_DB", "kpa_db")
        self.db_port = os.getenv("DB_PORT", "5432")

        self.DATABASE_URL = f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

        if not self.DATABASE_URL:
            logger.error("DATABASE_URL not configured properly.")
            sys.exit(1)

        try:
            self.engine = create_engine(self.DATABASE_URL, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
            self.Base = declarative_base()
            logger.info("✅ Database engine and session initialized successfully.")
        except SQLAlchemyError as e:
            logger.error(f"❌ Database connection failed: {e}")
            sys.exit(1)

    def get_session(self) -> Session:
        return self.SessionLocal()

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        session = self.get_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

# Singleton instance for app-wide use
db_instance = Database()

# Exported Base for model declaration
Base = db_instance.Base

# Exported FastAPI dependency
def get_db() -> Generator[Session, None, None]:
    db = db_instance.get_session()
    try:
        yield db
    finally:
        db.close()
