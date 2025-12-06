import streamlit as st
import pandas as pd

st.header("📊 รายงานยอดขายรายสาขา (Jan–Dec)")

uploaded_file = st.file_uploader("อัปโหลดไฟล์ยอดขาย (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ลำดับเดือน
    month_order = ["January","February","March","April","May","June","July",
                   "August","September","October","November","December"]

    df.columns = [str(c).strip() for c in df.columns]
    month_cols = [m for m in month_order if m in df.columns]

    # แปลงคอลัมน์เดือนให้เป็นตัวเลข
    for m in month_cols:
        df[m] = pd.to_numeric(df[m], errors="coerce").fillna(0)

    branch_list = df["Branch"].unique()
    selected_branch = st.selectbox("เลือกสาขา", branch_list)

    st.subheader(f"📍 ยอดขายสาขา: {selected_branch}")

    branch_data = df[df["Branch"] == selected_branch]

    display_df = branch_data[["Branch"] + month_cols].copy()
    display_df["Total"] = display_df[month_cols].sum(axis=1)

    # ⭐ แก้ ERROR: format เฉพาะคอลัมน์ตัวเลข
    numeric_cols = month_cols + ["Total"]
    styled_df = display_df.style.format("{:,.0f}", subset=numeric_cols)

    st.dataframe(styled_df)

    # สรุปยอดรายเดือน
    monthly_sum = branch_data[month_cols].sum()

    st.subheader("📈 กราฟแนวโน้มยอดขายรายเดือน")
    st.line_chart(monthly_sum)

    st.subheader("✨ สรุปผลรวมทั้งปี")
    col1, col2, col3 = st.columns(3)
    col1.metric("ยอดรวมทั้งปี", f"{monthly_sum.sum():,.0f} บาท")
    col2.metric("เดือนยอดสูงสุด", monthly_sum.idxmax())
    col3.metric("เดือนยอดต่ำสุด", monthly_sum.idxmin())
