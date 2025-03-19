from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import database, models

app = FastAPI()


# @app.get("/test")
# def testing(db: Session = Depends(database.get_db())):
#     pass