import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import pymongo
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

#Enable CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Connect to MongoDB
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client["test"]

@app.get("/")
async def root():
    return {"message": "Working"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
    
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)