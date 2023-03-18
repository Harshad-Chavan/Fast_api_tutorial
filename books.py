from fastapi import FastAPI

app = FastAPI()

@app.get("/api-endpoint")
def first_api():
    return {'message':'Hello Harshad'}