from fastapi import FastAPI, Depends, status, HTTPException
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
def get_tasks(db: Session = Depends(database.get_db)):
    tasks = db.query(models.Tasks).filter(models.Tasks.is_deleted == False).all()
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

    updated_task = task.model_dump() #if task is found, turn it into a dictionary
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
    # db.query(models.Tasks).filter(models.Tasks.id == id).update(task.is_deleted, synchronize_session=False)
    # commit to db
    db.commit()



# Pagination