import json
import plotly.colors as colors
from plotly.offline import iplot, init_notebook_mode
from matplotlib import cm
import matplotlib.animation as animation
import plotly.io as pio
import plotly.express as px
import numpy as np
from json import load
import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.graph_objects as go

st.set_page_config(layout="wide")


geojson_data = load(
    open('bangladesh_geojson_adm2_64_districts_zillas.json', 'r'))
geojson_data['features'][61].keys()
dff = pd.read_csv('final_report.csv')

district_id_map = {}
for feature in geojson_data["features"]:
    feature["id"] = feature["id"]
    district_id_map[feature["properties"]["ADM2_EN"]] = feature["id"]

default_value = None
dff['id'] = dff.District.apply(lambda x: district_id_map.get(x, default_value))
dff.to_csv('final_output.csv', index=False)
final_data = pd.read_csv('final_output.csv')
# final_data

# -------------------dividing time period------------------------


grouped1 = final_data.groupby(['id', 'LOCATION', 'District', 'time', 'time_of_day', 'day', 'week',
                               'month', 'year', 'Vehicle 1', 'lat', 'lon'])['Accidents'].sum().reset_index()
time_data = grouped1.copy()


grouped2 = final_data.groupby(['id', 'LOCATION', 'District', 'day', 'week', 'month', 'year',
                               'Vehicle 1', 'lat', 'lon'])['Accidents'].sum().reset_index()
# grouped2['Vehicle 1'] = grouped2['Vehicle 1'].fillna('No Data')
day_data = grouped2.copy()
# day_data


grouped3 = final_data.groupby(
    ['id', 'LOCATION', 'District', 'week', 'month', 'year', 'lat', 'lon'])['Accidents'].sum().reset_index()
week_data = grouped3.copy()


grouped4 = final_data.groupby(
    ['id', 'LOCATION', 'District', 'month', 'year', 'lat', 'lon'])['Accidents'].sum().reset_index()
month_data = grouped4.copy()
# month_data

grouped5 = final_data.groupby(['id', 'LOCATION', 'District', 'year', 'lat', 'lon'])[
    'Accidents'].sum().reset_index()
year_data = grouped5.copy()
# year_data

# ---------------------------------------------------streamlit-----------------
row1_col1, row1_col2, row1_col3 = st.columns(
    [0.5, 1.5, 1]
)
row2_col1, row2_col2, row2_col3 = st.columns(
    [0.5, 0.5, 2]
)
row3_col1, row3_col2, row3_col3, row3_col4 = st.columns(
    [0.5, 0.5, 0.5, 1.5]
)
row4_col1, row4_col2, row4_col3, row4_col4 = st.columns(
    [0.5, 0.5, 0.5, 1.5]
)
row5_col1, row5_col2 = st.columns(
    [1, 1]
)

row6_col1, row6_col2, row6_col3 = st.columns(
    [0.9, 0.1, 0.9]
)
row7_col1, row7_col2, row7_col3 = st.columns(
    [0.9, 0.1, 0.9]
)
row8_col1, row8_col2, row8_col3 = st.columns(
    [0.9, 0.1, 0.9]
)

# --------------------------------------------------------------------------------
with row1_col1:
    time_period = st.selectbox(
        "Select time period:", ["Daily", "Weekly", "Monthly", "Yearly"])


def year_func(yy):
    filtered = pd.DataFrame()
    for index, row in year_data.iterrows():
        if (row['year'] == yy):
            filtered = pd.concat([filtered, row.to_frame().T])
    return filtered


def month_func(yy, mm):
    filtered = pd.DataFrame()
    for index, row in month_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm)):
            filtered = pd.concat([filtered, row.to_frame().T])
    return filtered


def week_func(yy, mm, ww):
    filtered = pd.DataFrame()
    for index, row in week_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm) & (row['week'] == ww)):
            filtered = pd.concat([filtered, row.to_frame().T])
    return filtered


def day_func(yy, mm, dd):
    filtered = pd.DataFrame()
    for index, row in day_data.iterrows():
        if ((row['year'] == yy) & (row['month'] == mm) & (row['day'] == dd)):
            filtered = pd.concat([filtered, row.to_frame().T])
    return filtered


# def wday_func(yy, mm, ww, dd):
#     filtered = pd.DataFrame()
#     # time_data
#     for index, row in time_data.iterrows():
#         if ((row['year'] == yy) & (row['month'] == mm) & (row['week'] == ww) & (row['day'] == dd)):
#             filtered = pd.concat([filtered, row.to_frame().T])
#     return filtered


# ----------------------------------all parts-----------------------------


if time_period == "Yearly":
    with row2_col1:
        year = st.slider("Select year:", 2020, 2023, 2020)
    y = year
    filtered_data = year_func(y)

if time_period == "Monthly":
    with row2_col1:
        year = st.slider("Select year:", 2020, 2023, 2020)
    with row2_col2:
        month = st.slider("Select month:", 1, 12, 11)
    y = year
    m = month
    filtered_data = month_func(y, m)

if time_period == "Weekly":
    with row3_col1:
        year = st.slider("Select year:", 2020, 2023, 2020)
    with row3_col2:
        month = st.slider("Select month:", 1, 12, 11)
    with row3_col2:
        week = st.slider("Select week:", 1, 52, 1)
    y = year
    m = month
    w = week
    filtered_data = week_func(y, m, w)

if time_period == "Daily":
    with row4_col1:
        year = st.slider("Select year:", 2020, 2023, 2020)
    with row4_col2:
        month = st.slider("Select month:", 1, 12, 11)
    with row4_col3:
        day = st.slider("Select day of the month:", 1, 31, 1)
        # with row5_col1:
        #     show_day = st.checkbox('Show week:')
    y = year
    m = month
    d = day
    filtered_data = day_func(y, m, d)
    # if show_day:
    #     week = st.slider("Select week:", 1, 52, 1)
    #     w = week
    #     filtered_data = wday_func(y, m, w, d)

# ==================================================================


# =========================================================


if 'Accidents' in filtered_data:
    with row1_col3:
        total_accidents = filtered_data['Accidents'].sum()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total accident", total_accidents, total_accidents)
        col2.metric("Highest accident location", "9 mph", "-8 %")
        col3.metric("Humidity", "86%", "4 %")
        st.markdown('</div>', unsafe_allow_html=True)

    with row7_col1:
        # st.info("Deaths density by locations:")
        colorscale = [
            [0, "rgb(255, 255, 255)"],
            [0.1, "rgb(255, 235, 235)"],
            [0.2, "rgb(255, 205, 205)"],
            [0.3, "rgb(255, 175, 175)"],
            [0.4, "rgb(255, 145, 145)"],
            [0.5, "rgb(255, 115, 115)"],
            [0.6, "rgb(255, 85, 85)"],
            [0.7, "rgb(255, 55, 55)"],
            [0.8, "rgb(255, 25, 25)"],
            [0.9, "rgb(205, 0, 0)"],
            [1, "rgb(155, 0, 0)"]
        ]

        fig = go.Figure()

        fig.add_trace(go.Choroplethmapbox(
            geojson=geojson_data,
            locations=filtered_data['id'],
            z=filtered_data['Accidents'],
            colorscale=colorscale,
            zmin=filtered_data['Accidents'].min(),
            zmax=filtered_data['Accidents'].max(),
            marker_opacity=0.8,
            marker_line_width=0.6,
            marker_line_color='rgb(0, 0, 0)',
            text=filtered_data['District'],
            hovertemplate='<b>%{text}</b><br>Accidents: %{z}<extra></extra>'
        ))

        empty_locations = filtered_data[filtered_data['Accidents'] == 0]['id']
        for location in empty_locations:
            fig.data[0].hovertemplate = fig.data[0].hovertemplate.replace(
                location, f'{location}<br>Accidents: 0')

        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=6,
            mapbox_center={"lat": 23.6850, "lon": 90.3563},
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )

        fig.update_geos(fitbounds='locations', visible=True)
        fig.update_layout(
            height=600,
            width=700

        )

        st.plotly_chart(fig)

        # =========================================================

    with row6_col1:
        # st.info("Deaths density by districts:")
        color_scale = [
            "#F70D1A", "#F62817", "#E42217", "#E41B17", "#DC381F", "#C24641",
            "#C11B17", "#B22222", "#B21807", "#A52A2A", "#A70D2A", "#9F000F",
            "#931314", "#990000", "#990012", "#8B0000", "#800000", "#8C001A",
            "#7E191B", "#800517"
        ]
        m = folium.Map(location=[23.6850, 90.3563],
                       zoom_start=7, width="%60", height="%100")
        grouped_data = filtered_data.groupby(
            'LOCATION')['Accidents'].sum().reset_index()
        max_accidents = grouped_data['Accidents'].max()
        for index, row in grouped_data.iterrows():
            location = row['LOCATION']
            accidents = row['Accidents']
            LOCATION_data = filtered_data[filtered_data['LOCATION'] == location]
            for _, row in LOCATION_data.iterrows():
                lat = row['lat']
                lon = row['lon']
                scaling_factor = accidents / max_accidents
                max_radius = 50
                radius = scaling_factor * max_radius
                color_index = int(scaling_factor * (len(color_scale) - 1))
                color = color_scale[color_index]
                marker = folium.CircleMarker(
                    location=[lat, lon],
                    radius=radius,
                    color=color,
                    fill=True,
                    fill_color=color,
                    opacity=0.8
                )
                tooltip = f"Location: {location}<br>Total Accidents: {accidents}"
                marker.add_child(folium.Tooltip(tooltip))
                marker.add_to(m)
        map_html = m._repr_html_()
        st.components.v1.html(map_html, height=700, width=1000)

        # =====================================================
    with row8_col1:
        show_table = st.checkbox('Show table of data')

        if show_table:
            row6_col1, row6_col2, row6_col3 = [1, 1, 1]
            num_rows = len(filtered_data)
            page_size = 10
            num_pages = num_rows // page_size + \
                (1 if num_rows % page_size > 0 else 0)
            start_row = st.session_state.get('start_row', 0)
            current_page = start_row // page_size + 1 if start_row > 0 else 1
            start_row = max(0, min(num_rows - page_size, start_row))
            end_row = start_row + page_size if start_row + \
                page_size <= num_rows else num_rows
            table_data = filtered_data.iloc[start_row:end_row].to_html(
                index=False)
            table_style = '<style>table {margin: 0 auto;}</style>'
            container_style = '<style>.container {display: flex; justify-content: center;}</style>'

            st.session_state.start_row = start_row

            st.markdown(
                f'<div class="container" style="overflow-x:auto;">{table_style}{table_data}</div>', unsafe_allow_html=True)

            prev_disabled = start_row == 0
            next_disabled = end_row == num_rows
            if st.button("<", key="prev", disabled=prev_disabled):
                st.session_state.start_row = max(0, start_row - page_size)
            if st.button(">", key="next", disabled=next_disabled):
                st.session_state.start_row = min(
                    start_row + page_size, num_rows - page_size)

            start_row = st.session_state.get('start_row', 0)
            end_row = start_row + page_size if start_row + \
                page_size <= num_rows else num_rows
            page_info = f'<p>Showing rows {start_row+1}-{end_row} of {num_rows}</p>'

            st.markdown(
                f'<div class="container" style="text-align:center;">{page_info}</div>', unsafe_allow_html=True)

        # else:
        #     st.error('No data found !')


else:
    st.error('No data found !')
