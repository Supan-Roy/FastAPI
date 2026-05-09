from fastapi import FastAPI, HTTPException
from service.products import get_all_products

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Welcome to FastAPI"}

@app.get('/products')
def get_products():
    return get_all_products()
