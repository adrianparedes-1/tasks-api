from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from . import database, models, schemas

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
def testing(db: Session = Depends(database.get_db)):
    return {"test": "success"}


@app.get("/tasks")
def get_tasks(db: Session = Depends(database.get_db)):
    tasks = db.query(models.Tasks).all()
    return tasks


@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.Task, db: Session = Depends(database.get_db)):
    # turn input into dict
    print("hello")
    task_dict = models.Tasks(**task.model_dump())
    # task_dict = schemas.Task.model_dump(**task)
    print(task_dict)
    db.add(task_dict)
    db.flush()
    
    return task_dict