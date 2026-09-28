from fastapi import APIRouter,Depends,status  
from src.tasks import controller
from src.tasks.dtos import Task_schema,Task_response_schema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session
from src.utils.helpers import is_authenticated
from src.users.models import user_model


task_routes=APIRouter(prefix="/tasks")

@task_routes.post("/create",response_model=Task_response_schema,status_code=status.HTTP_201_CREATED)
def create_task(body:Task_schema,db:Session=Depends(get_db),user:user_model=Depends(is_authenticated)):
    return controller.create_task(body,db,user)


@task_routes.get("/all_tasks",response_model=List[Task_response_schema],status_code=status.HTTP_200_OK)
def get_all_tasks(db:Session=Depends(get_db),user:user_model=Depends(is_authenticated)):
    return controller.get_tasks(db,user)


@task_routes.get("/one_task/{task_id}",response_model=Task_response_schema,status_code=status.HTTP_200_OK)
def get_one_task(task_id:int,db:Session=Depends(get_db),user:user_model=Depends(is_authenticated)):
    return controller.get_one_task(task_id,db,user)

@task_routes.put("/update_task/{task_id}",response_model=Task_response_schema,status_code=status.HTTP_201_CREATED)
def update_task(body:Task_schema,task_id:int,db:Session=Depends(get_db),user:user_model=Depends(is_authenticated)):
    return controller.update_task(body,task_id,db,user)

@task_routes.delete("/delete_task/{task_id}",response_model=None,status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int,db:Session=Depends(get_db),user:user_model=Depends(is_authenticated)):
    return controller.delete_task(task_id,db,user)