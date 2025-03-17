

import csv
from fastapi import APIRouter
import os
import json
import pandas as pd
from utils.functions import get_csv_data, get_data_frame, get_summary_data, get_visual

router = APIRouter()

file_path = "/data/static/afghanistan.csv"


def strike_per_province():
    df = get_data_frame(file_path)
    return get_visual(df.sort_values(by="Province")["Province"].unique().tolist(), df.sort_values(by="Province").groupby(df["Province"])["Strike ID"].count().to_list(), title="Strikes per Province", chart_type="bar")

def strike_per_district():
    df = get_data_frame(file_path)
    return get_visual(df.sort_values(by="District")["District"].unique().tolist(), df.sort_values(by="District").groupby(df["District"])["Strike ID"].count().to_list(), title="Strikes per District", chart_type="bar")

def type_of_attack():
    df = get_data_frame(file_path)
    return get_visual(df.sort_values(by="Type of attack")["Type of attack"].unique().tolist(), df.sort_values(by="Type of attack").groupby(df["Type of attack"])["Strike ID"].count().to_list(), title="Type of attack", chart_type="pie")

def time_of_attack():
    df = get_data_frame(file_path)
    return get_visual(df.sort_values(by="Time")["Time"].unique().tolist(), df.sort_values(by="Time").groupby(df["Time"])["Strike ID"].count().to_list(), title="Time of attack", chart_type="pie")

def maximum_strikes():
    df = get_data_frame(file_path)
    return get_visual(None, df["Maximum strikes"].to_list(), title="Maximum strikes", chart_type="hist")

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
        "title": "US Airstrikes in Afghanistan",
        "description": "The dataset on US airstrikes in Afghanistan, sourced from Kaggle, provides a detailed record of individual strike events. Each entry represents a single strike and includes information such as the strike ID, date, location (village, district, province), type of attack, reported target, and casualty figures. This dataset is static because it represents a historical record of events that have already occurred and will not change. While the data was collected over a period of time, the final dataset represents a fixed collection of events.",
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
        "title":"Type of Attack",
        "image":type_of_attack(),
        },
        {
        "title":"Time of Attack",
        "image":time_of_attack(),
        },
        {
        "title":"Maximum number of strikes",
        "image":maximum_strikes(),
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