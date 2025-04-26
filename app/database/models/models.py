from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY  # Правильный импорт для PostgreSQL
from sqlalchemy.sql.sqltypes import Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    position = Column(String(50))
    embedding = Column(ARRAY(Float))  # Исправленный тип для PostgreSQL


class Detection(Base):
    __tablename__ = "detections"

    timestamp = Column(DateTime, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    camera_id = Column(String(20), nullable=False)
    photo_path = Column(String(255))