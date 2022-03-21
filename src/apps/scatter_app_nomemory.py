from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
from apps.scatter_vars import *
from app import app
from auth_settings import *
from authenticate import *

if auth_headers==None:
	layout = html.H3("Error authenticating with voyges api server. Check auth_settings.py")
else:
	r=requests.options(base_url+'voyage/?hierarchical=False',headers=auth_headers)
	md=json.loads(r.text)

	yr_range=range(1514,1866)
	markerstep=20

	layout = html.Div(children=[
		html.H3("NO MEMORY SCATTER APP -- DOWNLOADS SMALL CHUNK OF DATA FASTER BUT HAS TO RELOAD EVERY TIME YOU PRESS A BUTTON."),
		dcc.Graph(
			id='voyages-scatter-graph-nomemory'
		),
		html.Label('X variables'),
		dcc.Dropdown(
			id='x_vars',
			options=[{'label':md[i]['label'],'value':i} for i in scatter_plot_x_vars],
			value=scatter_plot_x_vars[0],
			multi=False
		),
			html.Label('Y variables'),
		dcc.Dropdown(
			id='y_vars',
			options=[{'label':md[i]['label'],'value':i} for i in scatter_plot_y_vars],
			value=scatter_plot_y_vars[0],
			multi=False
		),
			html.Label('Factors'),
		dcc.Dropdown(
			id='factors',
			options= [{'label':md[i]['label'],'value':i} for i in scatter_plot_factors],
			value=scatter_plot_factors[0],
			multi=False
		),
		html.Label('AVERAGE, SUM // OR SHOW INDIVIDUAL DATAPOINTS'),
		dcc.RadioItems(
					id='group_mode',
					options=[{'label': i, 'value': i} for i in ['AVERAGE BY FACTOR', 'SUM BY FACTOR','INDIVIDUAL DATAPOINTS']],
					value='SUM BY FACTOR',
					labelStyle={'display': 'inline-block'}
				),
			html.Label('Years'),
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
	Output('voyages-scatter-graph-nomemory', 'figure'),
	[Input('group_mode', 'value'),
	Input('x_vars', 'value'),
	Input('y_vars', 'value'),
	Input('factors', 'value'),
	Input('year-slider','value')]
	)

def update_figure(group_mode,x_val,y_val,color_val,yr):
	selected_fields=[x_val,y_val,color_val]
	url=base_url+'voyage/dataframes?hierarchical=False&voyage_dates__imp_arrival_at_port_of_dis_yyyy=%d,%d&selected_fields=%s' %(yr[0],yr[1],','.join(selected_fields))
	print(url)
	r=requests.get(url,headers=auth_headers)
	j=r.text
	df=pd.read_json(j)
	colors=df[color_val].unique()

	if group_mode != 'INDIVIDUAL DATAPOINTS':
		fig=go.Figure()
		for color in colors:
			df2=df.loc[df[color_val]==color]
			if group_mode=='AVERAGE BY FACTOR':
				df2=df2.groupby(x_val)[y_val].mean()
				figtitle='Stacked averages of '+ md[y_val]['label'] +' for each ' + md[color_val]['label'];
			elif group_mode=='SUM BY FACTOR':
				#print(df2)
				df2=df2.groupby(x_val)[y_val].sum()
				#print(df2)
				figtitle='Stacked totals of '+ md[y_val]['label'] +' for each ' + md[color_val]['label'];
			x_vals=[i for i in df2.index]
			y_vals=[df2[i] for i in x_vals]
			trace_name=color

			fig.add_trace(go.Scatter(
				x=x_vals,
				y=y_vals,
				name=trace_name,
				stackgroup='one',
				line= {'shape': 'spline'},
				mode='none')

			)
		fig.update_layout(
		xaxis_title=md[x_val]['label'],
		yaxis_title=md[y_val]['label'],
		transition_duration=200)

	else:
		df=df.fillna(0)
		fig = px.scatter(df,
		x=x_val,
		y=y_val,
		labels={x_val:md[x_val]['label'],y_val:md[y_val]['label'],color_val:md[color_val]['label']},
		color=color_val
		)
		fig.update_layout(transition_duration=500)
		figtitle="Data points represent individual voyages (zero for null entries)"

	fig.update_layout(
		title="Voyages: %s-%s<br>%s" %(str(yr[0]),str(yr[1]),figtitle),
		legend_title=md[color_val]['label']
	)
	#fig.write_html("scatter_nomem.html")	
	return fig
