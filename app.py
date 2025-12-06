import pandas as pd
import streamlit as st

# --- Load Branch List Sheet ---
branch_sheet_id = "1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E"
branch_url = f"https://docs.google.com/spreadsheets/d/{branch_sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"

branch_df = pd.read_csv(branch_url)

st.header("📍 เลือกสาขา")

branch_list = branch_df["Branch_Name"].tolist()
selected_branch = st.selectbox("เลือกสาขา", branch_list)

st.write("คุณเลือกสาขา:", selected_branch)
