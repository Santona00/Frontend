import streamlit as st
import json
import pandas as pd
import plotly.express as px

bd_districts = load(
    open('bangladesh_geojson_adm2_64_districts_zillas.json', 'r'))
bd_districts['features'][61].keys()
# bd_districts["features"][61]['properties']
dff = pd.read_csv('finaloutput.csv')
# len(dff)
# dff.head()
# print(dff)
# dff = pd.read_csv('finaloutput.csv')
# dff.head()
# print(dff)
dff['ACCIDENT Date'] = pd.to_datetime(dff['ACCIDENT Date'])
dff['week'] = pd.to_datetime(dff['ACCIDENT Date']).dt.isocalendar().week
dff['month'] = dff['ACCIDENT Date'].dt.month
dff['year'] = dff['ACCIDENT Date'].dt.year

# dff.head()
dff['LOCATION'] = dff['LOCATION'].str.title()
# dff.LOCATION

district_id_map = {}
for feature in bd_districts["features"]:
    feature["id"] = feature["id"]
    district_id_map[feature["properties"]["ADM2_EN"]] = feature["id"]
# district_id_map


# dff.LOCATION
default_value = None
dff['id'] = dff.LOCATION.apply(lambda x: district_id_map.get(x, default_value))
dff_copy = dff.copy()
dff_copy.head()


if 'date' in dff_copy.columns:
    dff_copy.drop(columns=['date'], inplace=True)
if 'time' in dff_copy.columns:
    dff_copy.drop(columns=['time'], inplace=True)

# Split the 'date_time' column into 'date' and 'time' columns
dff_copy['ACCIDENT Date'] = dff_copy['ACCIDENT Date'].apply(lambda x: str(x))

split_date_time = dff_copy['ACCIDENT Date'].str.split(' ', expand=True)
split_date_time.columns = ['date', 'time']
dff_copy = pd.concat([dff_copy, split_date_time[['date', 'time']]], axis=1)


dff_copy.head()
print(dff_copy)


# --------------------------------------
dff2_copy = dff_copy.copy()

dff2_copy.head()

dff3_copy = dff2_copy.copy()

dff3_copy.head()

dff3_copy.to_csv('output.csv', index=False)


color = cm.inferno_r(np.linspace(.3, .7, 64))


grouped = dff3_copy.groupby(['LOCATION', 'week', 'month', 'year']).size(
).reset_index(name='total_accidents')

print(grouped)

grouped = dff3_copy.groupby(['LOCATION', 'month', 'year']).size(
).reset_index(name='total_accidents')

print(grouped)

grouped = dff3_copy.groupby(['LOCATION', 'year']).size(
).reset_index(name='total_accidents')

print(grouped)


# Create a choropleth map using plotly.express library
fig = px.choropleth_mapbox(dff3_copy,
                           locations='id',
                           geojson=bd_districts,
                           color='count',
                           hover_name='LOCATION',
                           hover_data={'id': False, 'count': True},
                           # color_continuous_scale=['#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15'], # red sequential color scale
                           color_continuous_scale=['white', 'red'],
                           title='Bangladesh Accidents',
                           mapbox_style='carto-positron',
                           center={'lat': 23.6850, 'lon': 90.3563},
                           zoom=4.8,
                           opacity=0.6)
