from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Welcome to Todo App"}


@app.post("/todos/")
def create(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@app.get("/todos/")
def read_all(db: Session = Depends(get_db)):
    return crud.get_todos(db)


@app.get("/todos/{todo_id}")
def read_one(todo_id: int, db: Session = Depends(get_db)):
    return crud.get_todo(db, todo_id)


@app.delete("/todos/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db, todo_id)


@app.put("/todos/{todo_id}")
def update(todo_id: int, db: Session = Depends(get_db)):
    return crud.update_todo(db, todo_id)
