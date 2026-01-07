import pandas as pd
import os
from datetime import datetime

def generate_report(prompt: str, responses: dict):
    os.makedirs("data/comparsion_report",exist_ok=True)
    rows =[]
    for model, output in responses.items():
        rows.append({
            "Model":model,
            "Prompt":prompt,
            "Response":output,
            "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    df=pd.DataFrame(rows)
    df.to_csv("data/comparsion_report.csv", index=False)

    return "data/comparsion_report.csv"