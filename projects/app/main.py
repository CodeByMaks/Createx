from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .schemas import Book, BookCreate
from .crud import get_books, create_book
from .database import Base, engine
from .models import Book

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=Book)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)

@app.get("/books/", response_model=list[Book])
def list_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_books(db, skip, limit)
