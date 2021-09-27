import dash
import dash_core_components as dcc
import dash_html_components as html
from flask_apscheduler import APScheduler

from analysis_and_prediction.analysis_services.bot_analysis import dataframe_to_list, get_yahoo_data, prediction
from bot.bot_services.bot_services import log_mode_debug
from config.bot_config import config_yaml, chart_parameters, logger
from config.bot_config import fxcm_connection_config, fxcm_trading_config, yahoo_config

chart_parameters_config = chart_parameters(config_yaml)
begin_param = chart_parameters_config.begin
end_param = chart_parameters_config.end
fxcm_connection_configuration = fxcm_connection_config(config_yaml)
fxcm_trading_configuration = fxcm_trading_config(config_yaml)
yahoo_configuration = yahoo_config


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML" ])
app.config
scheduler = APScheduler()


@scheduler.task('interval', id='get-data', minutes=30)
def get_predictions_and_data():

    logger.info("##############################  Chart Analysis Started  ##############################")
    df = get_yahoo_data(yahoo_config.tickers)
    df.index = df.index.strftime('%Y/%m/%d %H:%M:%S')
    forecast = prediction(df)

    return forecast, df


forecast, df = get_predictions_and_data()


app.layout = html.Div(children=[

    html.Div(children=fxcm_trading_configuration.devises + ''' Chart Analysis. '''),

    dcc.Graph(
        id='trading-order',
        figure={
            "data": [
                {'x': forecast['ds'][begin_param:end_param], 'y': df['Close'][begin_param:end_param], 'type': 'line', 'name': 'Close Price'},
                {'x': forecast['ds'][begin_param:end_param], 'y': forecast['yhat_upper'][begin_param:end_param], 'type': 'line', 'name': 'Higher Line'},
                {'x': forecast['ds'][begin_param:end_param], 'y': forecast['yhat_lower'][begin_param:end_param], 'type': 'line', 'name': 'Lower Line'},
                {'x': forecast['ds'][begin_param:end_param], 'y': forecast['yhat'][begin_param:end_param], 'type': 'line', 'name': 'Median Line'},
                {'x': forecast['ds'][begin_param:end_param], 'y': forecast['trend'][begin_param:end_param], 'type': 'line', 'name': 'trend'}
            ],
            'layout': {
                'title': fxcm_trading_configuration.devises + ' Real Time Visualisation'
            },
        },
        style={'height': '100vh'}

    )
])


if __name__ == '__main__':
    log_mode_debug()
    logger.info("############  Get the data ###############")
    logger.info("############  forecast beginning ###############")
    yhat_upper = float(forecast['yhat_upper'].iloc[-2:-1])
    yhat_upper = '{0:.6f}'.format(yhat_upper)
    yhat_lower = float(forecast['yhat_lower'].iloc[-2:-1])
    yhat_lower = '{0:.6f}'.format(yhat_lower)
    yhat = float(forecast['yhat'].iloc[-2:-1])
    yhat = '{0:.6f}'.format(yhat)
    close = float(forecast['close'][-1:])
    close = '{0:.6f}'.format(close)
    logger.info("##############   Price: " + str(close) + "  ##############")
    logger.info("##############   yhat_upper: " + str(yhat_upper) + "  ##############")
    logger.info("##############  yhat_med: " + str(yhat) + "  ##############")
    logger.info("##############   yhat_lower: " + str(yhat_lower) + "  ##############")
    scheduler.init_app(app)
    scheduler.start()
    app.run_server(debug=True)
