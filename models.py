from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
Base = declarative_base()

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey('sessions.session_id'), nullable=False)
    original_filename = Column(String, nullable=False)
    converted_filename = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())