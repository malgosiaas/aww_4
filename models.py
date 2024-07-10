from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Picture(Base):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, index=True)
    rectangles = relationship("Rectangle", back_populates="picture")

class Rectangle(Base):
    __tablename__ = "rectangles"

    id = Column(Integer, primary_key=True, index=True)

    x1 = Column(Integer)
    x2 = Column(Integer)
    y1 = Column(Integer)
    y2 = Column(Integer)
    color = Column(String)
    picture_id = Column(Integer, ForeignKey("pictures.id"))
    picture = relationship("Picture", back_populates="rectangles")

