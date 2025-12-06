import streamlit as st
import pandas as pd

st.set_page_config(page_title="KingClass Dashboard", layout="wide")

# -----------------------------
# 1) CONFIG — Google Sheets URL
# -----------------------------
BRANCH_LIST_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/export?format=csv"
MASTER_DATA_URL = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM"

# -----------------------------
# 2) LOAD BRANCH LIST
# -----------------------------
@st.cache_data
def load_branch_list():
    df = pd.read_csv(BRANCH_LIST_URL)
    return df

branch_df = load_branch_list()
branch_list = branch_df["Branch_Name"].dropna().tolist()

# -----------------------------
# 3) PAGE TITLE
# -----------------------------
st.title("📍 เลือกสาขา")

# -----------------------------
# 4) SELECT BRANCH
# -----------------------------
selected_branch = st.selectbox("เลือกสาขา", branch_list)

st.write(f"คุณเลือก: **{selected_branch}**")

# -----------------------------
# 5) LOAD DATA FOR THIS BRANCH
# -----------------------------
@st.cache_data
def load_branch_data(branch_name):
    """
    ดึงข้อมูลจากแท็บชื่อสาขาในไฟล์ Master Dashboard
    ถ้าไม่มีแท็บ จะคืน None
    """
    try:
        sheet_url = MASTER_DATA_URL + f"/gviz/tq?tqx=out:csv&sheet={branch_name}"
        df = pd.read_csv(sheet_url)
        return df
    except:
        return None

data = load_branch_data(selected_branch)

# -----------------------------
# 6) CHECK IF DATA EXISTS
# -----------------------------
if data is None:
    st.warning("⛔ ยังไม่มีข้อมูลของสาขานี้ในระบบค่ะ\nกรุณาเพิ่มข้อมูลใน Google Sheet Master Data")
    st.stop()

# -----------------------------
# 7) CLEAN DATA (remove empty columns)
# -----------------------------
data = data.loc[:, ~data.columns.str.contains("Unnamed")]

# -----------------------------
# 8) SHOW DATA TABLE
# -----------------------------
st.subheader(f"📊 ข้อมูลยอดขายทั้งหมดของสาขา: {selected_branch}")
st.dataframe(data)

# -----------------------------
# 9) SUMMARY KPI — show latest year
# -----------------------------
latest_year = data["Year"].max()
latest_row = data[data["Year"] == latest_year].iloc[0]

total_latest = latest_row["Total"]
avg_month = latest_row[["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]].mean()

col1, col2 = st.columns(2)
col1.metric("ยอดขายรวมปีล่าสุด", f"{total_latest:,.0f} บาท")
col2.metric("ค่าเฉลี่ยรายเดือน", f"{avg_month:,.0f} บาท")

# -----------------------------
# 10) CHART — line graph for selected branch
# -----------------------------
st.subheader("📈 รายงานยอดขาย (ทุกปี)")

chart_df = data.set_index("Year")[
    ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
]

st.line_chart(chart_df.T)
