from fastapi import APIRouter

from models.todos import Todo
from config.database import todo_collection
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

#GET Request Method
@router.get("/")
async def get_todos():
    todos = list_serial(todo_collection.find())
    return todos


# POST Request Method
@router.post("/")
async def post_todo(todo: Todo):
    todo_collection.insert_one(dict(todo))

# PUT Request Method
@router.put("/{id}")
async def put_todo(id: str, todo: Todo):
    todo_collection.find_one_and_update({"_id":ObjectId(id)}, {"$set": dict(todo)})

# Delete Request Method
@router.delete("/{id}")
async def delete_todo(id: str):
    todo_collection.find_one_and_delete({"_id": ObjectId(id)})