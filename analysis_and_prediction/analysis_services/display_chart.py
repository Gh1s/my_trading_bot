import dash
import dash_core_components as dcc
import dash_html_components as html
from analysis_and_prediction.analysis_services.bot_analysis import get_data, prediction
from config.bot_config import yahoo_config, config_yaml, chart_parameters


chart_parameters_config = chart_parameters(config_yaml)
yahoo_configuration = yahoo_config(config_yaml)
df = get_data()
forecast = prediction(df)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
begin_param = chart_parameters_config.begin
end_param = chart_parameters_config.end


app.layout = html.Div(children=[
    html.H1(children='My Trading Bot'),

    html.Div(children='''
        Trading Bot Analisys.
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
