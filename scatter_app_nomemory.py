import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
from scatter_vars import *


import plotly.express as px

app = dash.Dash(__name__)
server=app.server
r=requests.options('http://127.0.0.1:8000/voyage/')
md=json.loads(r.text)
#print(md)

#print(df)

yr_range=range(1800,1850)
markerstep=5


app.layout = html.Div(children=[
	html.H3("NO MEMORY SCATTER APP -- DOWNLOADS SMALL CHUNK OF DATA FASTER BUT HAS TO RELOAD EVERY TIME YOU PRESS A BUTTON."),
    dcc.Graph(
        id='voyages-scatter-graph'
    ),
    html.Label('X variables'),
    dcc.Dropdown(
    	id='x_vars',
        options=[{'label':md[i]['label'],'value':i} for i in scatter_plot_x_vars],
        value='voyage_dates__imp_arrival_at_port_of_dis_year',
        multi=False
    ),
        html.Label('Y variables'),
    dcc.Dropdown(
    	id='y_vars',
        options=[{'label':md[i]['label'],'value':i} for i in scatter_plot_y_vars],
        value='voyage_slaves_numbers__imp_total_num_slaves_embarked',
        multi=False
    ),
        html.Label('Factors'),
    dcc.Dropdown(
    	id='factors',
        options= [{'label':md[i]['label'],'value':i} for i in scatter_plot_factors],
        value='voyage_itinerary__imp_port_voyage_begin',
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
        min=1800,
        max=1850,
        step=1,
        value=[1810,1815],
        marks={str(i*markerstep+yr_range[0]):str(i*markerstep+yr_range[0]) for i in range(int((yr_range[-1]-yr_range[0])/markerstep))}
    )
])



@app.callback(
	Output('voyages-scatter-graph', 'figure'),
	[Input('group_mode', 'value'),
	Input('x_vars', 'value'),
	Input('y_vars', 'value'),
	Input('factors', 'value'),
	Input('year-slider','value')]
	)

def update_figure(group_mode,x_val,y_val,color_val,yr):
	#filtered_df = df[df.year == selected_year]
	#selected_fields=[x_val,y_val,color_val]
	selected_fields=list(set(scatter_plot_x_vars+scatter_plot_y_vars+scatter_plot_factors))
	r=requests.get('http://127.0.0.1:8000/voyage/dataframes?voyage_dates__imp_arrival_at_port_of_dis_year=%d,%d&selected_fields=%s' %(yr[0],yr[1],','.join(selected_fields)))
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
				df2=df2.groupby(x_val)[y_val].sum()
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

	
	#fig.write_html('sample_scatter.html')
	
	return fig



if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=False,port=3500)