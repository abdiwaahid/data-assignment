import csv
import io
import json
import os
import matplotlib.pyplot as plt
import base64

import pandas as pd

def get_data_frame(file_path):
    df = pd.read_csv(os.getcwd()+file_path)
    df.map(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def get_csv_data(file_path):
    df = get_data_frame(file_path)
    return json.loads(df.to_json(orient="records"))

def get_summary_data(file_path):
    df = get_data_frame(file_path)
    columns =  df.columns
    summary = []
    for i, column in enumerate(columns):
        if df[column].dtype == 'int64':
            summary.append({
                'title': column,
                'sum': int(df[column].sum()),
            })
    return summary


def get_visual( x_axis, y_axis, title="",x_label="", y_label="", chart_type = 'line'):

    plt.figure(figsize=(20, 15))
    match chart_type:
        case "bar":
            plt.bar(x_axis, y_axis)
            plt.xticks(rotation=45, ha='right')
        case "line":
            plt.plot(x_axis, y_axis)
            plt.xticks(rotation=45, ha='right')
        case "pie":
            plt.pie(y_axis, startangle=140)
            plt.legend(x_axis, loc="lower right",fontsize=8,ncol=2)
        case 'hist':
            plt.hist(y_axis, bins=20)

    
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.tight_layout()

    img_stream = io.BytesIO()
    plt.savefig(img_stream, format="png")
    plt.close()

    img_stream.seek(0)
    img_bytes = img_stream.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    
    return img_base64