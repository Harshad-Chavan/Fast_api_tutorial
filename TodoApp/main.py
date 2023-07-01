# Depends stands for dependencies. when one fucntion os dependent on the
# execution of another func we use depends
import uvicorn
from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin, users

app = FastAPI()

# the line creates the .db sqlite file which contains database
models.Base.metadata.create_all(bind=engine)

# this tell adds the apis in different files
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
