import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import scatter_app,scatter_app_nomemory,sunburst_app,sunburst_app_nomemory

#FROM https://dash.plotly.com/urls#structuring-a-multi-page-app

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/scatter_app':
        return scatter_app.layout
    elif pathname == '/apps/scatter_app_nomemory':
        return scatter_app_nomemory.layout
    elif pathname == '/apps/sunburst_app':
        return sunburst_app.layout
    elif pathname == '/apps/sunburst_app_nomemory':
        return sunburst_app_nomemory.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)