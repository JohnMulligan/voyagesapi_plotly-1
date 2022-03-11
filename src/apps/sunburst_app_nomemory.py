from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
from apps.sunburst_vars import *
from app import app

r=requests.options('http://152.70.193.224:8000/voyage/?hierarchical=False')
md=json.loads(r.text)

yr_range=range(1514,1866)
markerstep=20

layout = html.Div(children=[
	html.H3("NO MEMORY SUNBURST APP -- DOWNLOADS SMALL DATAFRAME BUT HAS TO RELOAD EVERY TIME YOU PRESS A BUTTON -- STILL PREFERABLE IN THIS CASE"),
    dcc.Graph(
        id='voyages-sunburst-graph-nomemory'
    ),
    html.Label('Broad Region'),
    dcc.Dropdown(
    	id='broadregion',
        options=[{'label':md[i]['label'],'value':i} for i in geo_sunburst_broadregion_vars],
        value=geo_sunburst_broadregion_vars[0],
        multi=False
    ),
        html.Label('Region'),
    dcc.Dropdown(
    	id='region',
        options=[{'label':md[i]['label'],'value':i} for i in geo_sunburst_region_vars],
        value=geo_sunburst_region_vars[0],
        multi=False
    ),
        html.Label('Place'),
    dcc.Dropdown(
    	id='place',
        options= [{'label':md[i]['label'],'value':i} for i in geo_sunburst_place_vars],
        value=geo_sunburst_place_vars[0],
        multi=False
    ),
		html.Label('Numeric Values'),
	dcc.Dropdown(
    	id='numeric-values',
        options= [{'label':md[i]['label'],'value':i} for i in sunburst_plot_values],
        value=sunburst_plot_values[0],
        multi=False
    ),
    dcc.RangeSlider(
        id='year-slider',
        min=yr_range[0],
        max=yr_range[-1],
        step=1,
        value=[1800,1810],
        marks={str(i*markerstep+yr_range[0]):str(i*markerstep+yr_range[0]) for i in range(int((yr_range[-1]-yr_range[0])/markerstep))}
    )
])



@app.callback(
	Output('voyages-sunburst-graph-nomemory', 'figure'),
	[Input('broadregion', 'value'),
	Input('region', 'value'),
	Input('place', 'value'),
	Input('numeric-values', 'value'),
	Input('year-slider','value')]
	)
def update_figure(broadregion,region,place,numeric_values,yr):
	selected_fields=[broadregion,region,place,numeric_values]
	url='http://152.70.193.224:8000/voyage/dataframes?hierarchical=False&voyage_dates__imp_arrival_at_port_of_dis_yyyy=%d,%d&selected_fields=%s' %(yr[0],yr[1],','.join(selected_fields))
	print(url)
	r=requests.get(url)
	j=r.text
	df=pd.read_json(j)
	#print(df)
	df=df.fillna({i:"unknown" for i in [place,region,broadregion]})
	df=df.fillna({numeric_values:0})
	figtitle="Voyages: %d-%d" %(yr[0],yr[1])+ ", "+md[numeric_values]['label'] +' by:<br>'+ md[broadregion]['label'] +'<br>' + md[region]['label'] + '<br>' + md[place]['label']
	fig = px.sunburst(df,
		path=[broadregion,region,place],
		values=numeric_values,
		height=800,
	)
	fig.update_layout(transition_duration=500,title=figtitle)
	fig.write_html("sunburst_nomem.html")
	return fig
