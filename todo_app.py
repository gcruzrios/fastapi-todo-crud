
#python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define the Todo model using Pydantic
class Todo(BaseModel):
    id: int
    title: str
    completed: bool

# Initialize an empty list to store Todos
todos = []
@app.get('/', tags=["Inicio"])
def read_root():
    return {'message':'Hello world'}


@app.get("/api/todos/")
async def read_all_todos():
    return [{"id": i, "title": todo["title"], "completed": 
todo["completed"]} for i, todo in enumerate(todos)]

@app.post("/api/todos/")
async def create_todo(todo: Todo):
    new_todo = {"id": len(todos), "title": todo.title, "completed": False}
    todos.append(new_todo)
    return new_todo

@app.get("/api/todos/{todo_id}")
async def read_todo(todo_id: int):
    try:
        todo = next((todo for todo in todos if todo["id"] == todo_id))
        return {"id": todo["id"], "title": todo["title"], "completed": 
todo["completed"]}
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/api/todos/{todo_id}")
async def update_todo(todo_id: int, todo: Todo):
    try:
        existing_todo = next((todo for todo in todos if todo["id"] == 
todo_id))
        existing_todo["title"] = todo.title
        existing_todo["completed"] = todo.completed
        return {"id": todo_id, "title": todo.title, "completed": 
todo.completed}
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int):
    try:
        todo = next((todo for todo in todos if todo["id"] == todo_id))
        todos.remove(todo)
        return {"message": "Todo deleted"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo not found")
"""
This code defines a simple Todo list API with the following endpoints:

* `GET /api/todos/`: Returns a list of all Todos
* `POST /api/todos/`: Creates a new Todo
* `GET /api/todos/{todo_id}`: Returns a specific Todo by ID
* `PUT /api/todos/{todo_id}`: Updates a specific Todo by ID
* `DELETE /api/todos/{todo_id}`: Deletes a specific Todo by ID

You can run this code using the command `uvicorn todo_app:app --host 
0.0.0.0 --port 8000`, and then use a tool like `curl` or Postman to test 
the API.

For example, you could create a new Todo using:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"title": "Buy milk", 
"completed": false}' http://localhost:8000/api/todos/
```
And then retrieve that Todo using:
```bash
curl -X GET http://localhost:8000/api/todos/1
"""
