import streamlit as st
import pandas as pd

st.title("📊 KingClass Smart Report")

uploaded_file = st.file_uploader("อัปโหลดไฟล์ยอดขาย (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("อัปโหลดสำเร็จ!")
    st.dataframe(df)

    st.subheader("สรุปยอดรวม")
    st.write(df.sum(numeric_only=True))

    st.subheader("ตัวอย่างกราฟ")
    st.line_chart(df.select_dtypes(include=['number']))
