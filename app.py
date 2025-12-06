import streamlit as st
import pandas as pd

# -----------------------------
# 1) CONFIG URLs
# -----------------------------

BRANCH_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/export?format=csv"
MASTER_BASE = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/export?format=csv&gid="

# GID mapping (จากคุณนิก)
sheet_gid_map = {
    "B01": "539180310",
    "B02": "1398594410",
    "B03": "475910523",
}

# -----------------------------
# 2) INITIAL PAGE STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "overview"

if "selected_branch" not in st.session_state:
    st.session_state.selected_branch = None


# -----------------------------
# 3) LOAD 2567 (ALL BRANCHES)
# -----------------------------
def load_year_2567_all():
    all_rows = []

    for branch, gid in sheet_gid_map.items():
        try:
            df = pd.read_csv(MASTER_BASE + gid)
            row = df[df["Year"] == 2567].copy()

            if len(row) > 0:
                row["Branch"] = branch
                all_rows.append(row)

        except Exception as e:
            st.error(f"โหลดข้อมูลสาขา {branch} ไม่สำเร็จ: {e}")

    if not all_rows:
        return pd.DataFrame()

    df_all = pd.concat(all_rows, ignore_index=True)

    order = [
        "Branch", "JAN", "FEB", "MAR", "APR", "MAY",
        "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "Total"
    ]
    return df_all[order]


# -----------------------------
# 4) PAGE OVERVIEW
# -----------------------------
def page_overview():

    st.markdown("## 📊 ภาพรวมยอดขายทุกสาขา (ปี 2567)")
    st.markdown("### 🔎 คลิกชื่อสาขาเพื่อดูรายละเอียดยอดขาย")

    df_2567 = load_year_2567_all()

    if df_2567.empty:
        st.error("ไม่พบข้อมูลปี 2567")
        return

    # ทำลิงก์แบบคลิกได้
    df_show = df_2567.copy()
    df_show["Branch"] = df_show["Branch"].apply(
        lambda b: f"<a href='/?branch={b}' target='_self'>{b}</a>"
    )

    st.write(df_show.to_html(escape=False, index=False), unsafe_allow_html=True)

    # ตรวจ query param เมื่อคลิกสาขา
    params = st.query_params
    if "branch" in params:
        st.session_state.selected_branch = params["branch"]
        st.session_state.page = "detail"
        st.rerun()


# -----------------------------
# 5) PAGE DETAIL
# -----------------------------
def page_detail():

    branch = st.session_state.selected_branch
    st.markdown(f"## 📍 รายละเอียดสาขา {branch}")

    if branch not in sheet_gid_map:
        st.error("ไม่พบข้อมูลสาขานี้")
        return

    try:
        df = pd.read_csv(MASTER_BASE + sheet_gid_map[branch])
    except:
        st.error("โหลดข้อมูลไม่สำเร็จ")
        return

    st.write("### 📘 ยอดขายทุกปีของสาขานี้")
    st.dataframe(df, use_container_width=True)

    if st.button("⬅️ กลับหน้าหลัก"):
        st.session_state.page = "overview"
        st.session_state.selected_branch = None
        st.query_params.clear()
        st.rerun()


# -----------------------------
# 6) PAGE ROUTER
# -----------------------------
if st.session_state.page == "overview":
    page_overview()
else:
    page_detail()
