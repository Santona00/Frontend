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
import altair as alt
import calendar

# st.markdown("# Road Accident Analysis ")
st.sidebar.markdown("# See cumulative accident report")


row1_col1, row1_col2 = st.columns(
    [0.8, 2]
)
row2_col1, row2_col2 = st.columns(
    [1.5, 1.5]
)
row3_col1, row3_col2 = st.columns(
    [1.5, 1.5]
)

row4_col1, row4_col2, row4_col3 = st.columns(
    [1, 1, 1]
)
row5_col1, row5_col2 = st.columns(
    [1, 1]
)
row6_col1, row6_col2 = st.columns([4, 1])


def year_func3(yy):
    filtered3 = pd.DataFrame()
    for index, row in Mp.year_data.iterrows():
        if (row['year'] == yy):
            filtered3 = pd.concat([filtered3, row.to_frame().T])
    return filtered3


def month_func3(yy):
    filtered3 = pd.DataFrame()
    for index, row in Mp.month_data.iterrows():
        if (row['year'] == yy):
            filtered3 = pd.concat([filtered3, row.to_frame().T])
    return filtered3


with row1_col1:
    time_period3 = st.selectbox(
        "Select time period:", ["Monthly", "Yearly"])


if time_period3 == "Yearly":
    with row2_col1:
        year_range = st.slider("Select year range:", 2015, 2023, (2015, 2019))
        start_year, end_year = year_range
        filtered3_data = []
        years = []
        total_accidents = []
        cumulative_accidents = []
        for year in range(start_year, end_year + 1):
            data = year_func3(year)
            if data is not None and not data.empty:
                filtered3_data.append(data)
                years.append(year)
                total_accidents.append(data["total_accidents"].sum())
                cumulative_accidents.append(sum(total_accidents))
            else:
                st.write(f"No data found for year {year}")
        if len(filtered3_data) > 0:

            df_chart = pd.DataFrame(
                {"Year": years, "Cumulative Accidents": cumulative_accidents})

            base = alt.Chart(df_chart).encode(
                x=alt.X('Year:O', axis=alt.Axis(format='d', labelAngle=0)),
                y='Cumulative Accidents',
            )
            line = base.mark_line(point=True, color='red').encode(
                tooltip=[
                    alt.Tooltip('Year', title='Year'),
                    alt.Tooltip('Cumulative Accidents',
                                title='Cumulative Accidents', format='.2f')
                ]
            )
            text = base.mark_text(align='left', baseline='middle', dx=5, dy=-5).encode(
                text=alt.Text('Cumulative Accidents', format='.2f')
            )
            chart = (line + text).properties(
                width=850,
                height=700,
                title="Cumulative Accident Count / Year",

            )

            st.altair_chart(chart)


else:
    st.write("No data found for the selected year range.")


if time_period3 == "Monthly":
    with row3_col1:
        year = st.slider("Select year:", 2015, 2023, 2020)
        filtered3_data = month_func3(year)

        if filtered3_data is not None and not filtered3_data.empty:
            total_accidents = filtered3_data.groupby(
                'month')['total_accidents'].sum().cumsum().reset_index()

            chart = alt.Chart(total_accidents).mark_line(point=True, color='red').encode(
                x=alt.X('month', axis=alt.Axis(
                    labelAngle=0, format='d')),
                y='total_accidents',
                tooltip=[
                    alt.Tooltip('month', title='month'),
                    alt.Tooltip('total_accidents',
                                title='Cumulative Accidents', format='.2f')
                ]
            ).properties(
                width=850,
                height=700,
                title="Cumulative Accident Count / Month",
            )
            st.altair_chart(chart)

else:
    st.write("No data found for the selected year range.")
