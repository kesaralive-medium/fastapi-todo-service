import uuid

from datetime import datetime
from fastapi import APIRouter, Request, Response, status, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.Todo import Todo, GetTodo
from typing import List

router = APIRouter()


@router.post("/", response_description="create a todo", status_code=status.HTTP_201_CREATED, response_model=GetTodo)
def create_todo(request: Request, todo: Todo = Body(...)):
    try:
        todo = todo.dict()
        todo['_id'] = uuid.uuid4()
        todo['completed'] = False
        todo['created_at'] = datetime.utcnow()
        todo['updated_at'] = datetime.utcnow()
        todo = jsonable_encoder(todo)

        result = request.app.database['todos'].insert_one(todo)
        if result.inserted_id:
            todo = request.app.database['todos'].find_one({"_id": result.inserted_id})
            return todo
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create a todo.")
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create a todo.")


@router.get("/", response_description="get todos", status_code=status.HTTP_200_OK, response_model=List[GetTodo])
def get_todos(request: Request):
    if (todos := request.app.database['todos'].find()) is not None:
        return list(todos)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get todos.")


@router.put("/{todo_id}", response_description="update a todo", response_model=GetTodo)
def update_todo(request: Request, todo_id: uuid.UUID, todo: Todo = Body(...)):
    todo_id = str(todo_id)
    todo = todo.dict()
    update_query = {
        "$set": todo
    }

    result = request.app.database['todos'].update_one({"_id": todo_id}, update_query)
    updated_todo = request.app.database['todos'].find_one({"_id": todo_id})
    if result.modified_count > 0 or updated_todo is not None:
        return updated_todo
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")


@router.delete("/{todo_id}", response_description="delete a todo", status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response)
def delete_todo(request: Request, todo_id: uuid.UUID):
    todo_id = str(todo_id)
    result = request.app.database['todos'].delete_one({'_id': todo_id})
    if result.deleted_count > 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")


@router.post("/{todo_id}/complete", response_description="complete a todo", status_code=status.HTTP_200_OK,
             response_model=GetTodo)
def complete_todo(request: Request, todo_id: uuid.UUID):
    todo_id = str(todo_id)
    update_query = {
        "$set": {"completed": True}
    }
    result = request.app.database['todos'].update_one({"_id": todo_id}, update_query)
    updated_todo = request.app.database['todos'].find_one({"_id": todo_id})
    if result.modified_count > 0 or updated_todo is not None:
        return updated_todo
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")


@router.post("/{todo_id}/incomplete", response_description="withdraw a todo", status_code=status.HTTP_200_OK,
             response_model=GetTodo)
def withdraw_todo(request: Request, todo_id: uuid.UUID):
    todo_id = str(todo_id)
    update_query = {
        "$set": {"completed": False}
    }
    result = request.app.database['todos'].update_one({"_id": todo_id}, update_query)
    updated_todo = request.app.database['todos'].find_one({"_id": todo_id})
    if result.modified_count > 0 or updated_todo is not None:
        return updated_todo
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")


@router.get("/headers", response_description="get request headers")
def get_headers(request: Request):
    return request.headers
