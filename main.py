import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import routers.afghanistan as afghanistan
import routers.pakistan as pakistan
import routers.yemen as yemen
import routers.product as product
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from utils.functions import get_csv_data, get_summary_data, get_visual
app = FastAPI();

app.include_router(yemen.router,prefix="/api/static/yemen")
app.include_router(pakistan.router,prefix="/api/static/pakistan")
app.include_router(afghanistan.router,prefix="/api/static/afghanistan")

app.include_router(product.router,prefix="/api/time/product")

origins = [
    "http://localhost:4200",
    "http://localhost",
    "http://127.0.0.1:8000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/',  StaticFiles(directory='public',html=True), name='public')

@app.get("/{path}")
async def root():
    return RedirectResponse(url='/')
