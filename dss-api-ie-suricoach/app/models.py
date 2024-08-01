from sqlalchemy import Column, Integer, String, Float
from app.database import Base

# Model for accessing the database
class Review(Base):
    __tablename__ = 'f001sentiment'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250))
    sold = Column(Float)
    price = Column(Float)
    stock = Column(Float)
    comment = Column(String(250))
    kategori = Column(String(250))
    sentiment = Column(Integer)
