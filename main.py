from fastapi import FastAPI
from routes.route import router as todo_router
from routes.uploads import router as upload_router


app = FastAPI()

# Include routers
app.include_router(todo_router)
app.include_router(upload_router, prefix="/uploads")



