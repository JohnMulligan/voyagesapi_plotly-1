import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
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


r=requests.get('http://127.0.0.1:8000/voyage/table?&voyage_dates__imp_arrival_at_port_of_dis_year=1827,1829')

df=pd.read_json(r.text)
print(df)

x_val="voyage_dates__imp_arrival_at_port_of_dis_year"
y_val="voyage_slaves_numbers__imp_total_num_slaves_embarked"
color_val="voyage_itinerary__imp_port_voyage_begin"




'''fig = px.scatter(df,
	x=x_val,
	y=y_val,
	labels={x_val:md[x_val]['label'],y_val:md[y_val]['label'],color_val:md[color_val]['label']},
	color="voyage_itinerary__imp_port_voyage_begin"
	)'''
	

app.layout = html.Div(children=[
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
    	html.Label('Years'),
    dcc.Slider(
        id='year-slider',
        min=1800,
        max=1830,
        value=30,
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])

@app.callback(
	Output('voyages-scatter-graph', 'figure'),
	Input('x_vars', 'value'),
	Input('y_vars', 'value'),
	Input('factors', 'value')
	)
def update_figure(x_val,y_val,color_val):
    #filtered_df = df[df.year == selected_year]
        
    fig = px.scatter(df,
	x=x_val,
	y=y_val,
	labels={x_val:md[x_val]['label'],y_val:md[y_val]['label'],color_val:md[color_val]['label']},
	color=color_val
	)
    
    '''fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)'''

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True,port=3000)