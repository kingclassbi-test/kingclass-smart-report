import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ----------------- Google Sheets CSV URLs -----------------
BRANCH_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/export?format=csv&gid=0"
MASTER_BASE = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/export?format=csv&gid="

sheet_gid_map = {
    "B01": "539180310",
    "B02": "1398594410",
    "B03": "475910523",
}

# ==========================================================
# โหลดรายชื่อสาขา
# ==========================================================
branch_df = pd.read_csv(BRANCH_URL)
branch_list = branch_df["Branch_Name"].dropna().tolist()

# ==========================================================
# Session State สำหรับเก็บหน้าและสาขาที่เลือก
# ==========================================================
if "page" not in st.session_state:
    st.session_state.page = "overview"

if "selected_branch" not in st.session_state:
    st.session_state.selected_branch = None


# ==========================================================
# ฟังก์ชันเปลี่ยนหน้า (ใช้ JS เพื่อให้เปลี่ยนจริง)
# ==========================================================
def goto_detail(branch):
    st.session_state.selected_branch = branch
    st.session_state.page = "detail"


# ==========================================================
# โหลดข้อมูลเฉพาะปี 2567 ของทุกสาขา
# ==========================================================
def load_2567_all():
    rows = []
    for b, gid in sheet_gid_map.items():
        try:
            df = pd.read_csv(MASTER_BASE + gid)
            d67 = df[df["Year"] == 2567]
            if not d67.empty:
                row = d67.iloc[0].copy()
                row["Branch"] = b
                rows.append(row)
        except:
            pass

    if not rows:
        return pd.DataFrame()

    df_all = pd.DataFrame(rows)
    cols = ["Branch","JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","Total"]
    return df_all[cols]


# ==========================================================
# หน้า Overview (ตารางปี 2567 + คลิกเพื่อดูรายละเอียด)
# ==========================================================
def page_overview():
    st.title("📊 ภาพรวมยอดขายทุกสาขา (ปี 2567)")
    df = load_2567_all()

    if df.empty:
        st.warning("ไม่มีข้อมูลปี 2567")
        return

    # ทำปุ่มคลิกแทนลิงก์ <a> เพราะ Streamlit จับ event ได้ชัวร์กว่า
    st.write("### 🔍 คลิกสาขาเพื่อดูรายละเอียดยอดขาย")

    for i, row in df.iterrows():
        col1, col2 = st.columns([1, 12])
        if col1.button(row["Branch"]):
            goto_detail(row["Branch"])
            st.experimental_rerun()

    st.dataframe(df, use_container_width=True)


# ==========================================================
# หน้าแสดงรายละเอียดยอดขายของสาขา
# ==========================================================
def page_detail():
    branch = st.session_state.selected_branch
    st.title(f"📌 รายละเอียดสาขา {branch}")

    if branch not in sheet_gid_map:
        st.error("ไม่พบข้อมูลสาขา")
        return

    try:
        df = pd.read_csv(MASTER_BASE + sheet_gid_map[branch])
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"โหลดข้อมูลไม่สำเร็จ: {e}")

    if st.button("⬅️ กลับหน้าหลัก"):
        st.session_state.page = "overview"
        st.session_state.selected_branch = None
        st.experimental_rerun()


# ==========================================================
# ตัวควบคุมหน้า
# ==========================================================
if st.session_state.page == "overview":
    page_overview()
else:
    page_detail()
