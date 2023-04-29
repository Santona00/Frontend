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
st.sidebar.info(
    "Road Accidents"
)

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
row6_col1, row6_col2 = st.columns([4, 1])
# --------------------------------------------------------------------------------
with row1_col1:
    time_period2 = st.selectbox(
        "Select time period:", ["Monthly", "Yearly"])

# ---------------------------------------


def year_func2(yy):
    filtered2 = pd.DataFrame()
    for index, row in Mp.year_data.iterrows():
        if (row['year'] == yy):
            filtered2 = pd.concat([filtered2, row.to_frame().T])
    return filtered2


def month_func2(yy, mm):
    filtered2 = pd.DataFrame()
    for index, row in Mp.month_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm)):
            filtered2 = pd.concat([filtered2, row.to_frame().T])
    return filtered2



# ----------------------------------all parts-----------------------------
if time_period2 == "Yearly":
    with row2_col1:
        year_range = st.slider("Select year range:", 2020, 2023, (2020, 2021))
        start_year, end_year = year_range
        filtered2_data = []
        years = []
        Accidents = []
        for year in range(start_year, end_year + 1):
            data = year_func2(year)
            if data is not None and not data.empty:
                filtered2_data.append(data)
                years.append(year)
                Accidents.append(data["Accidents"].sum())
            else:
                st.write(f"No data found for year {year}")
        if len(filtered2_data) > 0:
            fig, ax = plt.subplots()
            ax.plot(years, Accidents, color='red')
            ax.set_xlabel("Years")
            ax.set_ylabel("Total Accidents")
            ax.set_title("Accident Count / Year")
            with row6_col1:
                # st.pyplot(fig)
                st.write(fig)

else:
    st.write("No data found for the selected year range.")

# -------------------------


   

