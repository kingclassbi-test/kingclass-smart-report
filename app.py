import pandas as pd

# 1) โหลด Branch List
sheet_id = "1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

branch_df = pd.read_csv(url)

branch_df
