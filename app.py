import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")  # ⭐ ทำให้หน้าเว็บกว้างเต็มจอ

MASTER_URL = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/export?format=csv&gid="
BRANCH_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqe07IQZXopvyLEeM6E/export?format=csv&gid=0"

# โหลดรายชื่อสาขา
branch_df = pd.read_csv(BRANCH_URL)
branch_list = branch_df["Branch_Name"].dropna().tolist()

branch_name = st.selectbox("เลือกสาขา", branch_list, key="branch")
st.write(f"คุณเลือก: **{branch_name}**")

# mapping gid
sheet_gid_map = {
    "B01": "539180310",
    "B02": "1398594410",
    "B03": "475910523",
}

if branch_name not in sheet_gid_map:
    st.error("ยังไม่มีข้อมูลสาขานี้ใน Master")
else:
    gid = sheet_gid_map[branch_name]
    url = MASTER_URL + gid
    df = pd.read_csv(url)

    st.subheader(f"📊 ยอดขายสาขา: {branch_name}")

    # ⭐⭐ ตารางเต็มจอ ไม่ต้องเลื่อน
    st.dataframe(df, use_container_width=True)
