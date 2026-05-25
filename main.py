from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

import crud, schemas, models
from database import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


# Author
@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def get_authors(
        skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return db.query(models.Author).offset(skip).limit(limit).all()


@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/authors/", response_model=schemas.AuthorResponse)
def create_author(
        author: schemas.AuthorCreate, db: Session = Depends(get_db)
):
    return crud.create_author(db, author)


# Book
@app.get("/books/", response_model=list[schemas.BookResponse])
def get_books(
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)

    if author_id:
        query = query.filter(models.Book.author_id == author_id)

    return query.offset(skip).limit(limit).all()
