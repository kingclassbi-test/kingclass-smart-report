import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# CONNECT GOOGLE SHEETS
# -----------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# -----------------------------
# LOAD BRANCH LIST
# -----------------------------
branch_sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/edit?usp=sharing"
)
branch_df = pd.DataFrame(branch_sheet.sheet1.get_all_records())

branch_list = branch_df["Branch_Name"].tolist()

# -----------------------------
# LOAD MASTER SHEET (ALL YEARS)
# -----------------------------
master = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/edit?usp=sharing"
)

# ดึงรายชื่อแท็บทั้งหมด แล้วสร้าง dict ที่ล้างช่องว่างให้สะอาด
raw_sheet_names = [ws.title for ws in master.worksheets()]
clean_name_map = {name.strip(): name for name in raw_sheet_names}

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("📍 เลือกสาขา")

selected_branch = st.selectbox("เลือกสาขา", branch_list)

# ตรวจสอบว่าแท็บของสาขานี้มีจริงหรือไม่
if selected_branch not in clean_name_map:
    st.warning("⛔ ยังไม่มีข้อมูลของสาขานี้ในระบบค่ะ กรุณาเพิ่มข้อมูลใน Google Sheet Master Data")
    st.stop()

# โหลดข้อมูลจากแท็บที่ถูกต้องจริงในไฟล์
true_sheet_name = clean_name_map[selected_branch]
sheet = master.worksheet(true_sheet_name)
df = pd.DataFrame(sheet.get_all_records())

st.subheader(f"คุณเลือก: {selected_branch}")
st.dataframe(df)
