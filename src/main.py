from fastapi import FastAPI
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="#SETUP_VARIABLES_Your_API_Name")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome!"}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')