from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import create_engine, select
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import models, schemas
from database import SessionLocal, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Annotated
import random, time

# uvicorn main:app --reload
# python -m http.server 5500



app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:8001",
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the database URL and create the engine
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/picture_from_database/{id}/")
def post_picture(
    id: int = id,
    db: Session = Depends(get_db)
):
    if id <= db.query(models.Picture).count():
        r = random.randint(1, 10)
        # r = 5
        if r == 1:
            raise ValueError("That word is not allowed here")
        if r == 2:
            return "example_large.json"
        if r == 3:
            time.sleep(3)
        id = db.query(models.Picture).count() - id + 1
        row = db.query(models.Picture).get({"id": id})
        picture_data = {
            "id": id,
            "rectangles": [{"x1": rect.x1, "x2": rect.x2, "y1": rect.y1, "y2":rect.y2, "color": rect.color} for rect in row.rectangles]
        }
        # return db.query(models.Rectangle).filter(models.Rectangle.image_id == id)
        return picture_data
    else:
        return {"end": True}

@app.get("/length/")
def post_picture(
    db: Session = Depends(get_db)
):
    return db.query(models.Picture).count()


@app.get("/images/")
def post_images(
    db: Session = Depends(get_db)
):
    # query = db.execute(select(
    # models.Picture.id,
    # models.Picture.rectangles
    # ).join(models.Picture.rectangles)).all()
    # print(query)
    # return query
    pictures = db.query(models.Picture).options(joinedload(models.Picture.rectangles)).all()

    results = []
    for picture in pictures:
        picture_data = {
            "id": picture.id,
            "rectangles": [{"x1": rect.x1, "x2": rect.x2, "y1": rect.y1, "y2":rect.y2, "color": rect.color} for rect in picture.rectangles]
        }
        results.append(picture_data)

    return results

@app.post("/save_image")
def save_image(image: schemas.Picture, db: Session = Depends(get_db)):
    img_db = models.Picture()
    db.add(img_db)
    db.commit()
    for rect in image.rectangles:
        rect_db = models.Rectangle(**rect.model_dump(), picture_id=img_db.id)
        db.add(rect_db)
    db.commit()
    db.expunge_all()
    db.close()
    return

@app.get('//')
def hello():
    return {"hello": "hello"}