import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# โหลด Branch List จาก Google Sheets
# -----------------------------
branch_url = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/export?format=csv"
branch_df = pd.read_csv(branch_url)

# ดึงชื่อสาขาเป็นรายการ dropdown
branch_list = branch_df["Branch_Name"].dropna().tolist()

# -----------------------------
# เริ่มหน้า UI
# -----------------------------
st.title("📍 เลือกสาขา")

selected_branch = st.selectbox("เลือกสาขา", branch_list)

st.write("คุณเลือก:", selected_branch)
