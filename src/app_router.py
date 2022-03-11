from dash import Dash, dcc, html, Input, Output, callback, dash_table
from app import app
#from apps import scatter_app_nomemory,sunburst_app_nomemory,estimates_table
from apps import scatter_app_nomemory,sunburst_app_nomemory
#FROM https://dash.plotly.com/urls#structuring-a-multi-page-app

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Go to Scatter App', href='/apps/scatter_app_nomemory'),
    html.Br(),
    dcc.Link('Go to Sunburst App', href='/apps/sunburst_app_nomemory'),
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/scatter_app_nomemory':
        return scatter_app_nomemory.layout
    elif pathname == '/apps/sunburst_app_nomemory':
        return sunburst_app_nomemory.layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True,port=3000)