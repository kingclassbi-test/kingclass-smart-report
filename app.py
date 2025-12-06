import pandas as pd
import streamlit as st

MASTER_URL = "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/export?format=csv&gid={gid}"
BRANCH_URL = "https://docs.google.com/spreadsheets/d/1mDVLSD2VWvIEX3pr68hdntZYtqeO7IQZXopvyLEeM6E/export?format=csv"

# 1) โหลด Branch List
branch_df = pd.read_csv(BRANCH_URL)
branch_list = branch_df["Branch_Name"].dropna().tolist()

st.selectbox("เลือกสาขา", branch_list, key="branch")
branch_name = st.session_state.branch

st.write("คุณเลือก:", branch_name)

# 2) ดึง gid ของแท็บใน Master ตามชื่อสาขา
sheet_gid_map = {
    "B01": "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/edit?gid=539180310#gid=539180310",      # https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/edit?gid=539180310#gid=539180310
    "B02": "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/edit?gid=1398594410#gid=1398594410", # https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/edit?gid=1398594410#gid=1398594410
    "B03": "https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/edit?gid=475910523#gid=475910523", # https://docs.google.com/spreadsheets/d/1kF_fBpWMoRgPPXjIhfZBI31xEoWvGKYJA4TTNYX1CIM/edit?gid=475910523#gid=475910523
}

if branch_name not in sheet_gid_map:
    st.error("ยังไม่มีข้อมูลสาขานี้ใน Master")
else:
    gid = sheet_gid_map[branch_name]
    url = MASTER_URL.format(gid=gid)

    df = pd.read_csv(url)
    st.dataframe(df)
