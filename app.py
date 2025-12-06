import streamlit as st
import pandas as pd

st.set_page_config(page_title="KingClass Smart Branch Dashboard", layout="wide")

# -----------------------------
# Utility: Convert Google Sheet URL → CSV URL
# -----------------------------
def to_csv_url(url):
    if "edit" in url:
        base = url.split("/edit")[0]
        return base + "/export?format=csv"
    return url

# -----------------------------
# 1) Load Branch List
# -----------------------------
BRANCH_LIST_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/edit?usp=sharing"
branch_csv = to_csv_url(BRANCH_LIST_URL)
branch_df = pd.read_csv(branch_csv)

# clean
branch_df.columns = branch_df.columns.str.strip()
branch_list = branch_df["Branch_Name"].dropna().unique().tolist()

# -----------------------------
# 2) Load Master Data (Each sheet has its own URL)
# -----------------------------
MASTER_URL = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/edit?usp=sharing"
MASTER_BASE = MASTER_URL.split("/edit")[0]

def load_branch_data(branch_name):
    """
    Loads a sheet by branch name.
    Converts spaces to %20 automatically.
    Returns DataFrame or None
    """
    safe_name = branch_name.replace(" ", "%20")
    sheet_url = f"{MASTER_BASE}/gviz/tq?tqx=out:csv&sheet={safe_name}"

    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

# -----------------------------
# UI
# -----------------------------
st.title("📊 KingClass Smart Report (Jan–Dec)")
st.write("เลือกสาขาที่ต้องการดูข้อมูล")

selected_branch = st.selectbox("เลือกสาขา", branch_list)

st.markdown(f"### 📍 สาขาที่เลือก: **{selected_branch}**")

# โหลดข้อมูลสาขา
df = load_branch_data(selected_branch)

if df is None or df.empty:
    st.warning("⚠️ ยังไม่มีข้อมูลของสาขานี้ใน Master Data หรือชื่อแท็บไม่ตรงกันค่ะ")
else:
    # แสดงข้อมูลทั้งหมด
    st.success("✔️ พบข้อมูลสาขานี้แล้ว")

    # แสดงปีล่าสุด (2567) แบบ Dashboard
    if "Year" in df.columns:
        latest_year = df["Year"].max()
        df_latest = df[df["Year"] == latest_year]

        st.markdown(f"## ⭐ ภาพรวมปี {latest_year}")
        st.dataframe(df_latest, use_container_width=True)

    # แสดงข้อมูลย้อนหลังทั้งหมด
    st.markdown("## 📘 ข้อมูลย้อนหลังทุกปี")
    st.dataframe(df, use_container_width=True)

    # กราฟรวม
    month_cols = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    for col in month_cols:
        if col not in df.columns:
            df[col] = 0

    df_plot = df.set_index("Year")[month_cols]

    st.line_chart(df_plot.T)
