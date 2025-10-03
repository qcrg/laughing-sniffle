from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import conf

Base = declarative_base()

class Product(Base):
  __tablename__ = "products"
  id = Column(Integer, primary_key=True, index=True, nullable=False)
  name = Column(String, index=True, nullable=False)
  basic_price = Column(Integer, nullable=False)
  product_price = Column(Integer, nullable=False)
  review_rating = Column(Integer, nullable=True)
  feedbacks = Column(Integer, nullable=False)
  quantity = Column(Integer, nullable=False)

engine = create_engine(conf.database.get_url())
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
