import streamlit as st
import pandas as pd

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(layout="wide")

# ----------------------------
# Custom CSS – make the page full width
# ----------------------------
st.markdown("""
<style>
.block-container { max-width: 100% !important; padding-left: 1rem; padding-right: 1rem; }
a { text-decoration: none !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Google Sheet URLs
# ----------------------------
BRANCH_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/export?format=csv"
MASTER_BASE = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/export?format=csv&gid="

# ----------------------------
# Load Branch List
# ----------------------------
branch_df = pd.read_csv(BRANCH_URL)
branch_list = branch_df["Branch_Name"].dropna().tolist()

# ----------------------------
# Mapping branch → gid
# ----------------------------
sheet_gid_map = {
    "B01": "539180310",
    "B02": "1398594410",
    "B03": "475910523",
}

# ----------------------------
# Initialize navigation state
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "overview"
if "selected_branch" not in st.session_state:
    st.session_state.selected_branch = None

def go_to_branch(b):
    st.session_state.selected_branch = b
    st.session_state.page = "detail"


# ============================================================
#                     📍 PAGE 1: OVERVIEW
# ============================================================
if st.session_state.page == "overview":

    st.title("📊 ภาพรวมยอดขายทุกสาขา (ปี 2567)")

    rows = []

    for branch in branch_list:
        if branch not in sheet_gid_map:
            continue

        gid = sheet_gid_map[branch]
        url = MASTER_BASE + gid
        df = pd.read_csv(url)

        df_2567 = df[df["Year"] == 2567]

        if df_2567.empty:
            continue

        row = df_2567.iloc[0].to_dict()
        row["Branch"] = branch

        rows.append(row)

    # Convert to DataFrame
    overview_df = pd.DataFrame(rows)

    # จัดคอลัมน์ให้อยู่ลำดับที่ต้องการ
    cols_order = ["Branch", "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                  "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "Total"]

    overview_df = overview_df[cols_order]

    # เปลี่ยนชื่อคอลัมน์ให้สวยงาม
    overview_df.rename(columns={"Branch": "สาขา", "Total": "ยอดรวมปี 2567"}, inplace=True)

    # 🔗 ทำให้ชื่อสาขาคลิกได้ (Link)
    def make_clickable(branch):
        return f'<a href="?branch={branch}">{branch}</a>'

    overview_df["สาขา"] = overview_df["สาขา"].apply(make_clickable)

    # แสดงเป็น HTML table (รองรับคลิก)
    st.write(overview_df.to_html(escape=False, index=False), unsafe_allow_html=True)


    # ตรวจจับ parameter จาก URL → ใช้สำหรับคลิก
    query_params = st.experimental_get_query_params()
    if "branch" in query_params:
        selected = query_params["branch"][0]
        go_to_branch(selected)


# ============================================================
#               📍 PAGE 2: Branch Detail Page
# ============================================================
elif st.session_state.page == "detail":

    branch = st.session_state.selected_branch
    st.title(f"📌 รายละเอียดยอดขายสาขา {branch}")

    gid = sheet_gid_map[branch]
    url = MASTER_BASE + gid
    df = pd.read_csv(url)

    st.dataframe(df, use_container_width=True)

    # ปุ่มกลับหน้าแรก
    if st.button("⬅️ กลับหน้าหลัก"):
        st.session_state.page = "overview"
        st.experimental_set_query_params()  # clear URL params
