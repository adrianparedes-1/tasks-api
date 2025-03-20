from fastapi import FastAPI, Depends, status, HTTPException
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
    new_task = models.Tasks(**task.model_dump())
    db.add(new_task)
    db.commit()
    
    return new_task


@app.get("/tasks/{id}")
def get_task(id: int, db: Session = Depends(database.get_db)):
    #query all and select first instance
    task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    #handle error if id is not found
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} was not found.")
    
    #return task with matching id
    return task

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(database.get_db)):
    # find task with matching id
    task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    print(task)
    # validate it exists and raise appropriate error
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} was not found.")
    # delete from db
    db.delete(task)
    # commit to db
    db.commit()


@app.put("/tasks/{id}")
def update_task(id: int, task: schemas.Task, db: Session = Depends(database.get_db)):
    #find task with with matching id and validate if it is found
    task_query = db.query(models.Tasks).filter(models.Tasks.id == id)
    # print(task_query)
    if not task_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} was not found.")
    # updated_task = models.Tasks(**task.model_dump())
    # the statement above is equivalent to doing models.Tasks(task.title=title, task.description=description, etc.)
    # the staement below just creates a dictionary from the task object
    updated_task = task.model_dump()
    task_query.update(updated_task, synchronize_session=False)
    db.commit()
    return updated_task