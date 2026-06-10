from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.responses import HTMLResponse
from auth import verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer

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

@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <html>
    <body>
        <h2>Todo App</h2>
        /todos/
            Title: <input type="text" name="title"><br><br>
            Description: <input type="text" name="description"><br><br>
            <button type="submit">Add Todo</button>
        </form>
    </body>
    </html>
    """

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User exists")
    return crud.create_user(db, user)


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_access_token({"sub": user.username})
    return {"access_token": token}

@app.get("/test")
def test():
    return {"message": "branch working"}
