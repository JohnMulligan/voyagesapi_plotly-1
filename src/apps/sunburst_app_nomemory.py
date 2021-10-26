import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
from apps.sunburst_vars import *
from app import app

r=requests.options('http://voyagesapi-django:8000/voyage/')
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
        value='voyage_itinerary__imp_broad_region_voyage_begin',
        multi=False
    ),
        html.Label('Region'),
    dcc.Dropdown(
    	id='region',
        options=[{'label':md[i]['label'],'value':i} for i in geo_sunburst_region_vars],
        value='voyage_itinerary__first_landing_region',
        multi=False
    ),
        html.Label('Place'),
    dcc.Dropdown(
    	id='place',
        options= [{'label':md[i]['label'],'value':i} for i in geo_sunburst_place_vars],
        value='voyage_itinerary__first_landing_place',
        multi=False
    ),
		html.Label('Numeric Values'),
	dcc.Dropdown(
    	id='numeric-values',
        options= [{'label':md[i]['label'],'value':i} for i in sunburst_plot_values],
        value='voyage_slaves_numbers__imp_total_num_slaves_embarked',
        multi=False
    ),
    dcc.RangeSlider(
        id='year-slider',
        min=yr_range[0],
        max=yr_range[-1],
        step=1,
        value=[1800,1850],
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
	r=requests.get('http://voyagesapi-django:8000/voyage/dataframes?&voyage_dates__imp_arrival_at_port_of_dis_year=%d,%d&selected_fields=%s' %(yr[0],yr[1],','.join(selected_fields)))
	j=r.text
	df=pd.read_json(j)
	df=df.fillna({i:"unknown" for i in geo_sunburst_broadregion_vars+geo_sunburst_region_vars+geo_sunburst_place_vars})
	figtitle="Voyages: %d-%d" %(yr[0],yr[1])+ ", "+md[numeric_values]['label'] +' by:<br>'+ md[broadregion]['label'] +'<br>' + md[region]['label'] + '<br>' + md[place]['label']
	fig = px.sunburst(df,
		path=[broadregion,region,place],
		values=numeric_values,
		height=800,
	)
	fig.update_layout(transition_duration=500,title=figtitle)
	#fig.write_html("sunburst_nomem.html")
	return fig
