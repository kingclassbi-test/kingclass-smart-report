import streamlit as st
import pandas as pd

# ---------------------------------------------------
# 🖥 ตั้งค่าหน้าเว็บแบบกว้าง
# ---------------------------------------------------
st.set_page_config(layout="wide")

# ---------------------------------------------------
# 🎨 CSS ขยายตารางให้เต็มหน้า
# ---------------------------------------------------
st.markdown("""
<style>
.block-container {
    max-width: 100% !important;
    padding-left: 1rem;
    padding-right: 1rem;
}
.stDataFrame, .dataframe {
    width: 100% !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 🔗 Google Sheets URLs
# ---------------------------------------------------
BRANCH_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/export?format=csv"
MASTER_BASE = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/export?format=csv&gid="

# ---------------------------------------------------
# 📌 โหลด Branch List
# ---------------------------------------------------
branch_df = pd.read_csv(BRANCH_URL)
branch_list = branch_df["Branch_Name"].dropna().tolist()

# ---------------------------------------------------
# 📌 Mapping: สาขา → gid (ต้องใส่ gid จริง)
# ---------------------------------------------------
sheet_gid_map = {
    "B01": "539180310",
    "B02": "1398594410",
    "B03": "475910523",
}

# ---------------------------------------------------
# 🧭 Navigation — ใช้ session_state
# ---------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "overview"
if "selected_branch" not in st.session_state:
    st.session_state.selected_branch = None

# ---------------------------------------------------
# 🔘 ฟังก์ชันไปหน้ารายละเอียดสาขา
# ---------------------------------------------------
def go_to_branch(branch):
    st.session_state.selected_branch = branch
    st.session_state.page = "detail"

# ---------------------------------------------------
# 📍 หน้า Overview — สรุปทุกสาขา ปี 2567
# ---------------------------------------------------
if st.session_state.page == "overview":

    st.title("📊 ภาพรวมยอดขายทุกสาขา (ปี 2567)")

    overview_rows = []

    for branch in branch_list:
        if branch not in sheet_gid_map:
            continue
        
        gid = sheet_gid_map[branch]
        url = MASTER_BASE + gid
        
        df = pd.read_csv(url)

        # ดึงเฉพาะปี 2567
        df_2567 = df[df["Year"] == 2567]

        if not df_2567.empty:
            total = df_2567["Total"].iloc[0]
        else:
            total = 0

        overview_rows.append({
            "สาขา": branch,
            "ยอดรวมปี 2567": total
        })

    overview_df = pd.DataFrame(overview_rows)

    st.dataframe(overview_df, use_container_width=True)

    st.write("### 🔍 คลิกสาขาที่ต้องการดูรายละเอียด")

    # สร้างปุ่มเลือกสาขาแบบคลิกได้
    for branch in branch_list:
        if branch in sheet_gid_map:
            if st.button(f"ดูรายละเอียดสาขา {branch}", key=f"btn_{branch}"):
                go_to_branch(branch)

# ---------------------------------------------------
# 📍 หน้า Detail — รายละเอียดทุกปีของสาขาที่เลือก
# ---------------------------------------------------
elif st.session_state.page == "detail":

    branch = st.session_state.selected_branch

    st.title(f"📍 รายละเอียดรายปีของสาขา {branch}")

    if branch not in sheet_gid_map:
        st.error("ยังไม่มีข้อมูลของสาขานี้ใน Master File")
    else:
        gid = sheet_gid_map[branch]
        url = MASTER_BASE + gid
        
        df = pd.read_csv(url)

        st.dataframe(df, use_container_width=True)

    # ปุ่มกลับหน้าหลัก
    st.button("⬅️ กลับหน้าหลัก", on_click=lambda: st.session_state.update({"page": "overview"}))
