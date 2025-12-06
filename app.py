import streamlit as st
import pandas as pd

BRANCH_LIST_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/export?format=csv"
MASTER_DATA_URL = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/export?format=csv&gid="

st.title("📍 เลือกสาขา")

# โหลด Branch list
branch_df = pd.read_csv(BRANCH_LIST_URL)
branch_list = branch_df["Branch_Name"].tolist()

# Dropdown เลือกสาขา
branch = st.selectbox("เลือกสาขา", branch_list)

st.write(f"คุณเลือก: **{branch}**")

# โหลดข้อมูลของสาขานี้
try:
    tab_url = f"https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/export?format=csv&sheet={branch}"
    df = pd.read_csv(tab_url)

    st.subheader(f"📊 ยอดขายสาขา: {branch}")
    st.dataframe(df)

except Exception:
    st.error("🚫 ยังไม่มีข้อมูลของสาขานี้ใน Master Data")
