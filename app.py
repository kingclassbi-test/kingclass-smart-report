{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
import plotly.express as px\
from openai import OpenAI\
import os\
\
# ---------------------------\
# PAGE CONFIG\
# ---------------------------\
st.set_page_config(\
    page_title="KingClass Smart Report",\
    layout="wide",\
    page_icon="\uc0\u55357 \u56522 "\
)\
\
# ---------------------------\
# LOAD LOGO\
# ---------------------------\
st.sidebar.image("assets/kingclass-logo.png", width=180)\
st.sidebar.markdown("### **KingClass Smart Report**")\
st.sidebar.markdown("---")\
\
# ---------------------------\
# OPENAI CLIENT\
# ---------------------------\
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))\
\
# ---------------------------\
# PAGE TITLE\
# ---------------------------\
st.markdown(\
    "<h1 style='color:#2F3A3D;'>\uc0\u55357 \u56522  KingClass AI Smart Report</h1>",\
    unsafe_allow_html=True\
)\
st.markdown(\
    "<p style='color:#3AA976; font-size:18px;'>\uc0\u3619 \u3632 \u3610 \u3610 \u3626 \u3619 \u3640 \u3611 \u3612 \u3621 \u3618 \u3629 \u3604 \u3586 \u3634 \u3618 \u3629 \u3633 \u3592 \u3593 \u3619 \u3636 \u3618 \u3632 \u3626 \u3635 \u3627 \u3619 \u3633 \u3610 \u3612 \u3641 \u3657 \u3610 \u3619 \u3636 \u3627 \u3634 \u3619  KingClass Academy</p>",\
    unsafe_allow_html=True\
)\
\
# ---------------------------\
# FILE UPLOADER\
# ---------------------------\
uploaded = st.file_uploader("\uc0\u3629 \u3633 \u3611 \u3650 \u3627 \u3621 \u3604 \u3652 \u3615 \u3621 \u3660 \u3618 \u3629 \u3604 \u3586 \u3634 \u3618  (.xlsx)", type=["xlsx"])\
\
if uploaded:\
    df = pd.read_excel(uploaded)\
\
    st.success("\uc0\u3650 \u3627 \u3621 \u3604 \u3586 \u3657 \u3629 \u3617 \u3641 \u3621 \u3626 \u3635 \u3648 \u3619 \u3655 \u3592  \u10004 ")\
\
    # ---------------------------\
    # METRICS\
    # ---------------------------\
    total_students = df["Total student"].sum()\
    total_tuition = df["Total Tuition Fee"].sum()\
\
    c1, c2 = st.columns(2)\
    c1.metric("\uc0\u55357 \u56424 \u8205 \u55356 \u57235  \u3609 \u3633 \u3585 \u3648 \u3619 \u3637 \u3618 \u3609 \u3626 \u3632 \u3626 \u3617 \u3607 \u3633 \u3657 \u3591 \u3627 \u3617 \u3604 ", f"\{total_students:,\}")\
    c2.metric("\uc0\u55357 \u56496  \u3619 \u3634 \u3618 \u3652 \u3604 \u3657 \u3626 \u3632 \u3626 \u3617 \u3607 \u3633 \u3657 \u3591 \u3627 \u3617 \u3604 ", f"\{total_tuition:,.2f\} \u3610 \u3634 \u3607 ")\
\
    # ---------------------------\
    # CHART: REGION\
    # ---------------------------\
    st.subheader("\uc0\u55357 \u56525  \u3619 \u3634 \u3618 \u3652 \u3604 \u3657 \u3605 \u3634 \u3617 \u3616 \u3634 \u3588  (Regional Performance)")\
\
    region_df = (\
        df.groupby("\uc0\u3616 \u3634 \u3588 ")[["Total student", "Total Tuition Fee"]]\
        .sum()\
        .reset_index()\
    )\
    fig_region = px.bar(\
        region_df,\
        x="\uc0\u3616 \u3634 \u3588 ", y="Total Tuition Fee",\
        color="Total Tuition Fee",\
        text_auto='.2s',\
        title="\uc0\u3618 \u3629 \u3604 \u3586 \u3634 \u3618 \u3619 \u3623 \u3617 \u3619 \u3634 \u3618 \u3616 \u3634 \u3588 ",\
        color_continuous_scale="greens"\
    )\
\
    st.plotly_chart(fig_region, use_container_width=True)\
\
    # ---------------------------\
    # CHART: TOP BRANCHES\
    # ---------------------------\
    st.subheader("\uc0\u55356 \u57286  Top 10 \u3626 \u3634 \u3586 \u3634 \u3618 \u3629 \u3604 \u3586 \u3634 \u3618 \u3626 \u3641 \u3591 \u3626 \u3640 \u3604 ")\
\
    top10 = df.sort_values("Total Tuition Fee", ascending=False).head(10)\
    fig_top = px.bar(\
        top10,\
        x="\uc0\u3594 \u3639 \u3656 \u3629 \u3626 \u3634 \u3586 \u3634 ",\
        y="Total Tuition Fee",\
        text_auto='.2s',\
        color="Total Tuition Fee",\
        color_continuous_scale="greens",\
        title="Top 10 Highest Revenue Branches"\
    )\
    st.plotly_chart(fig_top, use_container_width=True)\
\
    # ---------------------------\
    # AI INSIGHT\
    # ---------------------------\
    st.subheader("\uc0\u55358 \u56598  AI \u3623 \u3636 \u3648 \u3588 \u3619 \u3634 \u3632 \u3627 \u3660 \u3586 \u3657 \u3629 \u3617 \u3641 \u3621 ")\
\
    prompt = f"""\
    \uc0\u3623 \u3636 \u3648 \u3588 \u3619 \u3634 \u3632 \u3627 \u3660 \u3586 \u3657 \u3629 \u3617 \u3641 \u3621 \u3618 \u3629 \u3604 \u3586 \u3634 \u3618  KingClass Academy \u3592 \u3634 \u3585 \u3605 \u3634 \u3619 \u3634 \u3591 :\
\
    \{df.to_string()\}\
\
    \uc0\u3626 \u3619 \u3640 \u3611 \u3648 \u3611 \u3655 \u3609 \u3627 \u3633 \u3623 \u3586 \u3657 \u3629 \u3604 \u3633 \u3591 \u3609 \u3637 \u3657 :\
    1) \uc0\u3616 \u3634 \u3614 \u3619 \u3623 \u3617 \u3618 \u3629 \u3604 \u3586 \u3634 \u3618 \u3649 \u3621 \u3632 \u3592 \u3635 \u3609 \u3623 \u3609 \u3609 \u3633 \u3585 \u3648 \u3619 \u3637 \u3618 \u3609   \
    2) \uc0\u3626 \u3634 \u3586 \u3634 \u3607 \u3637 \u3656 \u3648 \u3604 \u3656 \u3609 \u3607 \u3637 \u3656 \u3626 \u3640 \u3604   \
    3) \uc0\u3616 \u3634 \u3588 \u3607 \u3637 \u3656 \u3648 \u3605 \u3636 \u3610 \u3650 \u3605 \u3648 \u3619 \u3655 \u3623 \u3607 \u3637 \u3656 \u3626 \u3640 \u3604   \
    4) \uc0\u3626 \u3634 \u3586 \u3634 \u3607 \u3637 \u3656 \u3617 \u3637 \u3588 \u3623 \u3634 \u3617 \u3648 \u3626 \u3637 \u3656 \u3618 \u3591   \
    5) \uc0\u3588 \u3635 \u3649 \u3609 \u3632 \u3609 \u3635 \u3648 \u3594 \u3636 \u3591 \u3585 \u3621 \u3618 \u3640 \u3607 \u3608 \u3660 \u3586 \u3629 \u3591  HQ  \
\
    \uc0\u3648 \u3586 \u3637 \u3618 \u3609 \u3649 \u3610 \u3610 \u3617 \u3639 \u3629 \u3629 \u3634 \u3594 \u3637 \u3614  \u3585 \u3619 \u3632 \u3594 \u3633 \u3610  \u3629 \u3656 \u3634 \u3609 \u3591 \u3656 \u3634 \u3618 \
    """\
\
    ai = client.chat.completions.create(\
        model="gpt-4o-mini",\
        messages=[\{"role":"user","content":prompt\}]\
    )\
\
    st.info(ai.choices[0].message["content"])\
\
    # ---------------------------\
    # AI CHATBOT\
    # ---------------------------\
    st.subheader("\uc0\u55357 \u56492  \u3606 \u3634 \u3617 \u3586 \u3657 \u3629 \u3617 \u3641 \u3621 \u3648 \u3614 \u3636 \u3656 \u3617 \u3648 \u3605 \u3636 \u3617 \u3592 \u3634 \u3585  AI")\
\
    user_q = st.text_input("\uc0\u3606 \u3634 \u3617 \u3629 \u3632 \u3652 \u3619 \u3585 \u3655 \u3652 \u3604 \u3657  \u3648 \u3594 \u3656 \u3609  '\u3626 \u3634 \u3586 \u3634 \u3652 \u3627 \u3609 \u3586 \u3634 \u3618 \u3604 \u3637 \u3607 \u3637 \u3656 \u3626 \u3640 \u3604 ?'")\
\
    if user_q:\
        q_prompt = f"""\uc0\u3651 \u3594 \u3657 \u3586 \u3657 \u3629 \u3617 \u3641 \u3621 \u3609 \u3637 \u3657 \u3651 \u3609 \u3585 \u3634 \u3619 \u3605 \u3629 \u3610 \u3588 \u3635 \u3606 \u3634 \u3617 :\
\
        \{df.to_string()\}\
\
        \uc0\u3588 \u3635 \u3606 \u3634 \u3617 : \{user_q\}\
        \uc0\u3605 \u3629 \u3610 \u3651 \u3627 \u3657 \u3648 \u3586 \u3657 \u3634 \u3651 \u3592 \u3591 \u3656 \u3634 \u3618  \u3594 \u3633 \u3604 \u3648 \u3592 \u3609 \
        """\
\
        ans = client.chat.completions.create(\
            model="gpt-4o-mini",\
            messages=[\{"role":"user","content":q_prompt\}]\
        )\
\
        st.success(ans.choices[0].message["content"])}