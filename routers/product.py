

import csv
from fastapi import APIRouter
import os
import json
import pandas as pd
from utils.functions import get_csv_data, get_data_frame, get_summary_data, get_visual

router = APIRouter()

file_path = "/data/time/ppi_dataset.csv"

def strike_per_province():
    df = get_data_frame(file_path)
    return get_visual(df.sort_values(by="Province")["Province"].unique().tolist(), df.sort_values(by="Province").groupby(df["Province"])["Strike ID"].count().to_list(), title="Strikes per Province", chart_type="bar")

def type_of_attack():
    df = get_data_frame(file_path)
    return get_visual(df.sort_values(by="Type of attack")["Type of attack"].unique().tolist(), df.sort_values(by="Type of attack").groupby(df["Type of attack"])["Strike ID"].count().to_list(), title="Type of Attack", chart_type="pie")

def confirmed_possible():
    df = get_data_frame(file_path)
    return get_visual(df.sort_values(by="Confirmed/\npossible US attack?")["Confirmed/\npossible US attack?"].unique().tolist(), df.sort_values(by="Confirmed/\npossible US attack?").groupby(df["Confirmed/\npossible US attack?"])["Strike ID"].count().to_list(), title="Confirmed or Possible US attack?", chart_type="pie")

def maximum_strikes():
    df = get_data_frame(file_path)
    return get_visual(None, df["Maximum number of strikes"].to_list(), title="Maximum number of strikes", chart_type="hist")

def maximum_people_killed():
    df = get_data_frame(file_path)
    return get_visual(None, df["Maximum people killed"].to_list(), title="Maximum People Killed", chart_type="hist")

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
        "title": "US Airstrikes in Yemen",
        "description": "The US airstrikes in Yemen dataset follows the same structure as the Afghanistan and Pakistan datasets, providing a record of individual strike events with details on the date, location, target, and casualties. Like the other two datasets, this dataset is static, representing a historical record of completed airstrikes. The data represents a fixed set of events that have occurred in the past.",
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
        "title":"Confirmed or Possible US attack?",
        "image":confirmed_possible(),
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