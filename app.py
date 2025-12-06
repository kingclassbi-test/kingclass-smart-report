import streamlit as st
import pandas as pd

st.header("📊 รายงานยอดขายรายสาขา (Jan–Dec)")

uploaded_file = st.file_uploader("อัปโหลดไฟล์ยอดขาย (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ลำดับเดือน
    month_order = ["January","February","March","April","May","June","July",
                   "August","September","October","November","December"]

    # ทำความสะอาดชื่อคอลัมน์
    df.columns = [str(c).strip() for c in df.columns]

    # ระบุคอลัมน์เดือนที่มีอยู่จริงในไฟล์
    month_cols = [m for m in month_order if m in df.columns]

    # แปลงคอลัมน์เดือนเป็นตัวเลข (ถ้าแปลงไม่ได้ ให้เป็น 0)
    for m in month_cols:
        df[m] = pd.to_numeric(df[m], errors="coerce").fillna(0)

    # Dropdown เลือกสาขา
    branch_list = df["Branch"].unique()
    selected_branch = st.selectbox("เลือกสาขา", branch_list)

    st.subheader(f"📍 ยอดขายสาขา: {selected_branch}")

    branch_data = df[df["Branch"] == selected_branch]

    # ตารางสรุป Jan–Dec
    display_df = branch_data[["Branch"] + month_cols].copy()
    display_df["Total"] = display_df[month_cols].sum(axis=1)

    st.dataframe(display_df.style.format("{:,.0f}"))

    # สรุปยอดรวมรายเดือนเพื่อทำกราฟ
    monthly_sum = branch_data[month_cols].sum()

    st.subheader("📈 กราฟแนวโน้มยอดขายรายเดือน")
    st.line_chart(monthly_sum)

    # KPI สรุปทั้งปี
    st.subheader("✨ สรุปผลรวมทั้งปี")
    col1, col2, col3 = st.columns(3)
    col1.metric("ยอดรวมทั้งปี", f"{monthly_sum.sum():,.0f} บาท")
    col2.metric("เดือนยอดสูงสุด", monthly_sum.idxmax())
    col3.metric("เดือนยอดต่ำสุด", monthly_sum.idxmin())
