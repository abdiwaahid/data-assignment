

import csv
from fastapi import APIRouter
import os
import json
import pandas as pd
from utils.functions import get_csv_data, get_data_frame, get_summary_data, get_visual

router = APIRouter()

file_path = "/data/static/pakistan.csv"


def strike_per_province():
    df = get_data_frame(file_path)
    return get_visual(df.sort_values(by="Area")["Area"].unique().tolist(), df.sort_values(by="Area").groupby(df["Area"])["Strike ID"].count().to_list(), title="Strikes per Area", chart_type="bar")

def strike_per_province():
    df = get_data_frame(file_path)
    return get_visual(df.sort_values(by="Location")["Location"].unique().tolist(), df.sort_values(by="Location").groupby(df["Location"])["Strike ID"].count().to_list(), title="Strikes per Location", chart_type="bar")

def maximum_people_killed():
    df = get_data_frame(file_path)
    return get_visual(None, df["Maximum total people killed"].to_list(), title="Maximum total people killed", chart_type="hist")

def maximum_civilians_killed():
    df = get_data_frame(file_path)
    return get_visual(None, df["Maximum civilians reported killed"].to_list(), title="Maximum civilians reported killed", chart_type="hist")

def maximum_children_killed():
    df = get_data_frame(file_path)
    return get_visual(None, df["Maximum children reported killed"].to_list(), title="Maximum children reported killed", chart_type="hist")

def strikes_over_time():
    df = get_data_frame(file_path)
    df['Date'] = pd.to_datetime(df['Date'],format='%d/%m/%Y')
    df['Month'] = df['Date'].dt.to_period('M')
    return get_visual(df.sort_values(by="Month")["Month"].unique().astype(str).tolist(), df.sort_values(by="Month").groupby(df["Month"])["Strike ID"].count().to_list(), title="Strikes over time", chart_type="line")


@router.get("/info")
async def get_info():
    return {
        "title": "US Airstrikes in Pakistan",
        "description": "Similar to the Afghanistan dataset, the US airstrikes in Pakistan dataset contains information on individual strike events. It includes details such as the date, location, type of attack, reported target, and casualty figures. This dataset is also static because it represents a completed historical record of strikes conducted in Pakistan. The data is a snapshot of events that have already happened, and the information is not subject to change.",
    }

@router.get("/data")
async def get_data():
    return {"data": get_csv_data(file_path)}


@router.get("/summary")
async def get_summary():
    return get_summary_data(file_path)



@router.get("/visuals")
async def get_visuals():
    return {"data": [
        {
        "title":"Strikes per Province",
        "image":strike_per_province(),
        },
        {
        "title":"Maximum People Killed",
        "image":maximum_people_killed(),
        },
        {
        "title":"Maximum civilians reported killed",
        "image":maximum_civilians_killed(),
        },
        {
        "title":"Maximum children reported killed",
        "image":maximum_children_killed(),
        },
        {
        "title":"Strikes over time",
        "image":strikes_over_time()
        }
    ]}