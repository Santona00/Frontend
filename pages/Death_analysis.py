import matplotlib.animation as animation
import matplotlib.pyplot as plt
import streamlit as st
import plotly.colors as colors
from plotly.offline import iplot, init_notebook_mode
from matplotlib import cm
import plotly.io as pio
import plotly.express as px
import numpy as np
from json import load
import pandas as pd
import streamlit as st
import matplotlib.cm as cm
import pydeck as pdk
import Map as Mp
st.markdown("# Road Accident Analysis ")
st.sidebar.markdown("# Analysis Report ")

row1_col1, row1_col2 = st.columns(
    [0.8, 2]
)
row2_col1, row2_col2 = st.columns(
    [1.5, 1.5]
)
row3_col1, row3_col2, row3_col3 = st.columns(
    [1, 1, 1]
)
row4_col1, row4_col2, row4_col3 = st.columns(
    [1, 1, 1]
)
row5_col1, row5_col2 = st.columns(
    [1, 1]
)
# --------------------------------------------------------------------------------
with row1_col1:
    time_period2 = st.selectbox(
        "Select time period:", ["Daily", "Weekly", "Monthly", "Yearly"])

# --------------------------------------- check if each row satisfies the condition


def year_func2(yy):
    # create an empty DataFrame to hold the filtered2 data
    filtered2 = pd.DataFrame()
    for index, row in Mp.year_data.iterrows():
        if (row['year'] == yy):
            # if the condition is satisfied, add the row to the filtered DataFrame
            filtered2 = pd.concat([filtered2, row.to_frame().T])
    return filtered2


def month_func2(yy, mm):
    filtered2 = pd.DataFrame()
    for index, row in Mp.month_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm)):
            filtered2 = pd.concat([filtered2, row.to_frame().T])
    return filtered2


def week_func2(yy, mm, ww):

    filtered2 = pd.DataFrame()
    for index, row in Mp.week_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm) & (row['week'] == ww)):
            filtered2 = pd.concat([filtered2, row.to_frame().T])
    return filtered2


def day_func2(yy, mm, dd):
    filtered2 = pd.DataFrame()
    for index, row in Mp.day_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm) & (row['day'] == dd)):
            filtered2 = pd.concat([filtered2, row.to_frame().T])
    return filtered2


def wday_func2(yy, mm, ww, dd):
    filtered2 = pd.DataFrame()
    for index, row in Mp.time_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm) & (row['week'] == ww) & (row['day'] == dd)):
            filtered2 = pd.concat([filtered2, row.to_frame().T])
    return filtered2
# ----------------------------------all parts-----------------------------


if time_period2 == "Yearly":
    with row2_col1:
        year_range = st.slider("Select year range:", 2015, 2023, (2015, 2019))
        start_year, end_year = year_range
        filtered2_data = []
        for year in range(start_year, end_year + 1):
            data = year_func2(year)
            if data is not None and not data.empty:
                filtered2_data.append(data)
            else:
                st.write(f"No data found for year {year}")

if len(filtered2_data) > 0:
    table_data = pd.concat(filtered2_data)
    page_size = 10
    num_pages = len(table_data) // page_size + 1
    page_num = st.session_state.get("page_num", 0)

    st.table(table_data.iloc[page_num * page_size: (page_num + 1) * page_size])

    col1, col2, col3 = st.columns(3)
    if page_num > 0:
        if col2.button("<< Previous"):
            page_num -= 1
            st.session_state["page_num"] = page_num
    if page_num < num_pages - 1:
        if col3.button("Next >>"):
            page_num += 1
            st.session_state["page_num"] = page_num
else:
    st.write("No data found for the selected year range.")


# st.pyplot(fig)


# -------------------------

if time_period2 == "Monthly":
    with row2_col1:
        year = st.slider("Select year:", 2015, 2023, 2020)
    with row2_col2:
        month = st.slider("Select month:", 1, 12, 11)
    y = year
    m = month
    filtered2_data = month_func2(y, m)

if time_period2 == "Weekly":
    with row3_col1:
        year = st.slider("Select year:", 2015, 2023, 2020)
    with row3_col2:
        month = st.slider("Select month:", 1, 12, 11)
    with row3_col3:
        week = st.slider("Select week:", 1, 52, 1)
    y = year
    m = month
    w = week
    filtered2_data = week_func2(y, m, w)

if time_period2 == "Daily":
    with row4_col1:
        year = st.slider("Select year:", 2015, 2023, 2020)
    with row4_col2:
        month = st.slider("Select month:", 1, 12, 11)
    with row4_col3:
        day = st.slider("Select day of the month:", 1, 31, 1)
        with row5_col1:
            show_day = st.checkbox('Show week:')
    y = year
    m = month
    d = day
    filtered2_data = day_func2(y, m, d)
    if show_day:
        week = st.slider("Select week:", 1, 52, 1)
        w = week
        filtered2_data = wday_func2(y, m, w, d)
