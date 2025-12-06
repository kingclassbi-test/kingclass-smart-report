import streamlit as st
import pandas as pd

st.header("📊 รายงานยอดขายรายสาขา (Jan–Dec)")

# โหลดไฟล์จากผู้ใช้
uploaded_file = st.file_uploader("อัปโหลดไฟล์ยอดขาย (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ตรวจสอบและแปลงคอลัมน์เดือนให้เป็นลำดับถูกต้อง
    month_order = ["January","February","March","April","May","June","July","August","September","October","November","December"]

    # ทำให้ชื่อคอลัมน์เหมือนกัน (กรณีใช้ชื่อไทยหรือรูปแบบอื่น)
    df.columns = [str(c).strip() for c in df.columns]

    # เลือกเฉพาะคอลัมน์เดือน + สาขา
    month_cols = [m for m in month_order if m in df.columns]

    # dropdown เลือกสาขา
    branch_list = df["Branch"].unique()
    selected_branch = st.selectbox("เลือกสาขา", branch_list)

    # กรองข้อมูลเฉพาะสาขา
    branch_data = df[df["Branch"] == selected_branch]

    # แสดงตาราง Jan–Dec
    st.subheader(f"📍 ยอดขายสาขา: {selected_branch}")

    display_df = branch_data[["Branch"] + month_cols].copy()
    display_df["Total"] = display_df[month_cols].sum(axis=1)

    st.dataframe(display_df.style.format("{:,.0f}"))

    # ทำกราฟรายเดือน
    monthly_sum = branch_data[month_cols].sum()

    st.line_chart(monthly_sum)

    # KPI Summary
    st.subheader("✨ สรุปผลทั้งปี")

    col1, col2, col3 = st.columns(3)
    col1.metric("ยอดรวมทั้งปี", f"{monthly_sum.sum():,.0f} บาท")
    col2.metric("เดือนที่สูงสุด", monthly_sum.idxmax())
    col3.metric("เดือนที่ต่ำสุด", monthly_sum.idxmin())
