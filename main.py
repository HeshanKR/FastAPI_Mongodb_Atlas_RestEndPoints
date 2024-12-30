from fastapi import FastAPI
from routes.route import router as todo_router
from routes.uploads import router as upload_router
from config.database import client


app = FastAPI()

# Include routers
app.include_router(todo_router)
app.include_router(upload_router, prefix="/uploads")


# from fastapi.lifecycle import Lifespan

# def app_lifespan(app: FastAPI) -> Lifespan:
#     """
#     Lifespan function to handle startup and shutdown events.
#     """
#     async def startup():
#         print("Application startup: MongoDB connection initialized.")

#     async def shutdown():
#         print("Application shutdown: Closing MongoDB connection.")
#         client.close()

#     return startup, shutdown

# app = FastAPI(lifespan=app_lifespan)




# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# uri = "mongodb+srv://3214heshan:jgNJp2CDyRyZsPKw@modellacluster.u5r6h.mongodb.net/?retryWrites=true&w=majority&appName=ModellaCluster"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

