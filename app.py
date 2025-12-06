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

# ----------------- Load branch list -----------------
branch_df = pd.read_csv(BRANCH_URL)
branch_list = branch_df["Branch_Name"].dropna().tolist()

# ----------------- Navigation state -----------------
if "page" not in st.session_state:
    st.session_state.page = "overview"
if "selected_branch" not in st.session_state:
    st.session_state.selected_branch = None

def go_to_branch(b):
    st.session_state.selected_branch = b
    st.session_state.page = "detail"

# ----------------- Function to load 2567 data for all branches -----------------
def load_year_2567_all():
    rows = []
    for branch, gid in sheet_gid_map.items():
        try:
            df = pd.read_csv(MASTER_BASE + gid)
            df_67 = df[df["Year"] == 2567]
            if not df_67.empty:
                r = df_67.iloc[0].copy()
                r["Branch"] = branch
                rows.append(r)
        except Exception as e:
            st.error(f"Error loading branch {branch}: {e}")
    if not rows:
        return pd.DataFrame()
    df_all = pd.DataFrame(rows)
    cols = ["Branch", "JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","Total"]
    return df_all[cols]

# ----------------- PAGE: Overview -----------------
def page_overview():
    st.title("📊 ภาพรวมยอดขายทุกสาขา (ปี 2567)")
    st.write("🔍 คลิกชื่อสาขาเพื่อดูรายละเอียดยอดขาย")
    df_67 = load_year_2567_all()

    if df_67.empty:
        st.warning("ยังไม่มีข้อมูลยอดขายปี 2567")
        return

    df_show = df_67.copy()
    df_show["Branch"] = df_show["Branch"].apply(lambda b: f'<a href="?branch={b}">{b}</a>')

    st.write(df_show.to_html(escape=False, index=False), unsafe_allow_html=True)

    params = st.experimental_get_query_params()
    if "branch" in params:
        b = params["branch"][0]
        if b in sheet_gid_map:
            go_to_branch(b)
            st.experimental_set_query_params()  # clear params

# ----------------- PAGE: Detail -----------------
def page_detail():
    branch = st.session_state.selected_branch
    st.title(f"📌 รายละเอียดสาขา {branch}")

    if branch not in sheet_gid_map:
        st.error("ไม่พบข้อมูลสาขาใน Master Data")
    else:
        try:
            df = pd.read_csv(MASTER_BASE + sheet_gid_map[branch])
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"โหลดข้อมูลไม่สำเร็จ: {e}")

    if st.button("⬅️ กลับหน้าหลัก"):
        st.session_state.page = "overview"
        st.session_state.selected_branch = None
        st.experimental_set_query_params()

# ----------------- Router -----------------
if st.session_state.page == "overview":
    page_overview()
else:
    page_detail()
