from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session
from . import database, models, schemas

app = FastAPI()

#testing ---------------
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
def testing(db: Session = Depends(database.get_db)):
    return {"test": "success"}

# Basic CRUD operations ------------------------------
@app.get("/tasks")
def get_tasks(offset: PositiveInt, page_limit: PositiveInt, db: Session = Depends(database.get_db)):
    tasks = db.query(models.Tasks).filter(models.Tasks.is_deleted == False).offset(offset).limit(page_limit).all()
    return tasks


@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.Task, db: Session = Depends(database.get_db)):
    # turn input into dict
    
    new_task = task.model_dump(exclude_unset=True)
    new_task.pop("offset", None)
    new_task.pop("page_limit", None)
    task_model = models.Tasks(**new_task)
    print(task_model)
    db.add(task_model)
    db.commit()
    
    return task_model


@app.get("/tasks/{id}")
def get_task(id: int, db: Session = Depends(database.get_db)):
    #query all and select first instance
    task = db.query(models.Tasks).filter(models.Tasks.id == id).filter(models.Tasks.is_deleted == False).first()
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
    if not task_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} was not found.")

    updated_task = task.model_dump(exclude_unset=True) #if task is found, turn it into a dictionary
    task_query.update(updated_task, synchronize_session=False) # use update method and pass the newly created dict
    db.commit()
    return updated_task


# ---------------------------------------------------

# Soft Delete

@app.put("/tasks/soft/{id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_task(id: int, db: Session = Depends(database.get_db)):
    # find task with matching id
    task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    # validate it exists and raise appropriate error
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} was not found.")
    # instead of deleting from db, just update the is_deleted field to True
    task.is_deleted = True
    # commit to db
    db.commit()



