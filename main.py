from fastapi import FastAPI
from database import Base, engine
from routers import auth_router, transaction_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(auth_router.router)
app.include_router(transaction_router.router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}