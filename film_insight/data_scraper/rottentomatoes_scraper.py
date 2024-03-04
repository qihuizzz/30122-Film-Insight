import os
import time
import pandas as pd
import requests
import json


output_file = "data/rottentomatoes_data.xlsx"
data = pd.read_excel("data/rottentomatoes_url.xlsx")


def get_url_and_save(url, name, time_year, output_file):
    all_data = []
    # set the headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    }

    response = requests.get(url=url, headers=headers)

    data = json.loads(response.text)

    # extract the data
    extracted_data = [
        {
            "name": name,
            "quote": review["quote"],
            "score": review.get("score", "Not provided"),
            "time": time_year,
        }
        for review in data["reviews"]
    ]

    all_data.extend(extracted_data)
    print(all_data)
    # save the data to an Excel file
    df = pd.DataFrame(all_data)
    if os.path.exists(output_file):
        with pd.ExcelWriter(
            output_file, engine="openpyxl", mode="a", if_sheet_exists="overlay"
        ) as writer:
            df.to_excel(
                writer,
                index=False,
                header=False,
                startrow=writer.sheets["Sheet1"].max_row,
            )
    else:
        df.to_excel(output_file, index=False)


for index, row in data.iterrows():
    time.sleep(1)
    name = row["Movie Title"]
    url = row["url"]
    time_year = row["year"]
    get_url_and_save(url, name, time_year, output_file)
    print(url, "end", "-" * 30)
