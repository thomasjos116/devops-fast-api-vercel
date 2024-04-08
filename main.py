# -*- coding: utf-8 -*-
"""
This is a BackEnd package written in Python and FASTAPI
"""
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from recommend import recommend_college, data_read

class user_input(BaseModel):
    cao_points : str
    city_name : str
    field_interest : str
    hobbies : str
    spending_limit : str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/recommend")

def operate(input:user_input):

    data, cities, job_interest, hobby_interest = data_read()

    result = recommend_college(input.spending_limit, input.cao_points, input.city_name, input.hobbies, input.field_interest)
    return result