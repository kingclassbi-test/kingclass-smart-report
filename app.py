import streamlit as st
import pandas as pd

# ---------------------------------------------------
# 🔧 ตั้งค่าให้หน้าเว็บแสดงแบบกว้างเต็มจอ
# ---------------------------------------------------
st.set_page_config(layout="wide")

# ---------------------------------------------------
# 🎨 CSS บังคับขยายตารางให้เต็มหน้า
# ---------------------------------------------------
st.markdown("""
<style>
/* container ใหญ่สุดของ Streamlit */
.block-container {
    max-width: 100% !important;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* ให้ DataFrame/table ขยายเต็มความกว้าง */
.stDataFrame, .dataframe {
    width: 100% !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# 🔗 URLs ของ Google Sheets (CSV Export)
# ---------------------------------------------------
BRANCH_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/export?format=csv"
MASTER_BASE = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/export?format=csv&gid="


# ---------------------------------------------------
# 📌 โหลด Branch List
# ---------------------------------------------------
branch_df = pd.read_csv(BRANCH_URL)
branch_list = branch_df["Branch_Name"].dropna().tolist()

st.title("📍 เลือกสาขา")

branch_name = st.selectbox("เลือกสาขา", branch_list)

st.write("### คุณเลือก:", branch_name)


# ---------------------------------------------------
# 📌 Map: ชื่อสาขา → gid ของแท็บใน Master File
# ---------------------------------------------------
sheet_gid_map = {
    "B01": "539180310",         # gid ของแท็บ B01
    "B02": "1398594410",    # ใส่ gid จริงของคุณแทนที่
    "B03": "475910523",    # ใส่ gid จริงของคุณแทนที่
}


# ---------------------------------------------------
# ❌ ถ้าไม่มี gid → แจ้งเตือน
# ---------------------------------------------------
if branch_name not in sheet_gid_map:
    st.error("ยังไม่มีข้อมูลสาขานี้ใน Master Data")
else:
    gid = sheet_gid_map[branch_name]
    master_url = MASTER_BASE + gid

    # โหลดข้อมูลจากแท็บของสาขานั้น
    df = pd.read_csv(master_url)

    st.write(f"### 📊 ยอดขายสาขา: {branch_name}")

    # ---------------------------------------------------
    # 🎯 แสดงตารางแบบเต็มจอ
    # ---------------------------------------------------
    st.dataframe(df, use_container_width=True)
