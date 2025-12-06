import pandas as pd
import streamlit as st

# ---------------------------
# 1) Google Sheet CSV URLs
# ---------------------------

BRANCH_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/export?format=csv&gid=0"

MASTER_BASE = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/export?format=csv&gid="

# ---------------------------
# 2) กำหนด gid ของแต่ละสาขา
# (จากแท็บใน Master Sheet)
# ---------------------------

sheet_gid_map = {
    "B01": "539180310",          # gid ของ B01
    "B02": "1398594410",     # ตัวอย่าง gid (ให้ใส่จริงตามไฟล์)
    "B03": "475910523",  # gid ของ B03 (จากที่นิกให้มา)
}

# ---------------------------
# 3) โหลด Branch List
# ---------------------------

branch_df = pd.read_csv(BRANCH_URL)
branch_list = branch_df["Branch_Name"].dropna().tolist()

st.title("📌 เลือกสาขา")

branch_name = st.selectbox("เลือกสาขา", branch_list)

st.subheader(f"คุณเลือก: **{branch_name}**")

# ---------------------------
# 4) ตรวจสอบว่ามี gid ของสาขานี้ไหม
# ---------------------------

if branch_name not in sheet_gid_map:
    st.error("⛔ ยังไม่มีข้อมูลสาขานี้ใน Master Data")
    st.stop()

gid = sheet_gid_map[branch_name]

# URL สำหรับ Master Data ของแต่ละสาขา
MASTER_URL = MASTER_BASE + gid

# ---------------------------
# 5) โหลดข้อมูลจาก Master
# ---------------------------

try:
    df = pd.read_csv(MASTER_URL)
except Exception as e:
    st.error("⛔ โหลดข้อมูลไม่สำเร็จ โปรดตรวจสอบ gid หรือสิทธิ์การเข้าถึง Google Sheet")
    st.write(e)
    st.stop()

# ---------------------------
# 6) แสดงตารางเต็มหน้า (Wide mode)
# ---------------------------

st.write("### 📊 ยอดขายสาขา:", branch_name)

# ทำให้ตารางเต็มหน้าจอโดยใช้ CSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# แสดงตาราง
st.dataframe(df, use_container_width=True)
