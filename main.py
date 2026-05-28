from fastapi import FastAPI
from task_routers import task
from database import Base, engine
from task_models import Task 
from task_routers import users

app  = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get("/")
def main():
    return {"status":"App is running"}


app.include_router(task.router)
app.include_router(users.router)

# if __name__ == "__main__":
#     main()
