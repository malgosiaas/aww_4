from pydantic import BaseModel
from typing import List

class Rectangle(BaseModel):
    x1: int
    x2: int
    y1: int
    y2: int
    color: str

class Picture(BaseModel):
    rectangles: List[Rectangle]

class ImageReading(BaseModel):
    id: int
    rectangles: List[Rectangle]

    class Config:
        orm_mode = True

class RectangleReading(BaseModel):
    id: int
    x1: int
    x2: int
    y1: int
    y2: int
    color: str
    image_id: int

    class Config:
        orm_mode = True
