import dash
import dash_core_components as dcc
import dash_html_components as html
from main import df, forecast
from config.bot_config import chart_parameters, config_yaml


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
begin_param = chart_parameters(config_yaml).begin
end_param = chart_parameters(config_yaml).end


app.layout = html.Div(children=[
    html.H1(children='My Trading Bot'),

    html.Div(children='''
        Trading Bot Analisis.
    '''),

    dcc.Graph(
        id='trading-order',
        figure={
            "data": [
                {'x': forecast['ds'][begin_param:end_param], 'y': df['Close'][begin_param:end_param], 'type': 'line', 'name': 'price'},
                {'x': forecast['ds'][begin_param:end_param], 'y': forecast['yhat_upper'][begin_param:end_param], 'type': 'line', 'name': 'high level'},
                {'x': forecast['ds'][begin_param:end_param], 'y': forecast['yhat_lower'][begin_param:end_param], 'type': 'line', 'name': 'price'},
                {'x': forecast['ds'][begin_param:end_param], 'y': forecast['yhat'][begin_param:end_param], 'type': 'line', 'name': 'price'}
            ],
            'layout': {
                'title': 'Dash Data Visualisation'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)