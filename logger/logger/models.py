import datetime

from sqlalchemy import (
    Column, DateTime, Integer, String, Float
)
from sqlalchemy.ext.declarative import declarative_base


class Base(object):
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )


DeclarativeBase = declarative_base(cls=Base)


class Order(DeclarativeBase):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cc = Column(String, nullable=False)
    type = Column(String, nullable=False)
    price = Column(Float)
    quantity = Column(Float)
