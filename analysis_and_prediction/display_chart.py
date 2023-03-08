import dash
import dash_core_components as dcc
import dash_html_components as html
#from flask_apscheduler import APScheduler
from analysis_and_prediction.analysis_services.bot_analysis import prediction
#from bot.bot_services.bot_services import log_mode_debug
from config.bot_config import Config, logger
import fxcmpy


chart_parameters_config = Config().chart_parameters
begin_param = chart_parameters_config.begin
end_param = chart_parameters_config.end
fxcm_connection_configuration = Config().fxcm_connection_config
fxcm_trading_configuration = Config().fxcm_trading_config


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML" ])
app.config
#scheduler = APScheduler()


#@scheduler.task('interval', id='get-data', minutes=30)
def get_predictions_and_data():

    logger.info("##############################  Chart Analysis Started  ##############################")
    connexion = fxcmpy.fxcmpy(access_token=fxcm_connection_configuration.token,
                              log_level="error",
                              server=fxcm_connection_configuration.server_mode,
                              log_file=fxcm_connection_configuration.log_file)
    df = connexion.get_candles(fxcm_trading_configuration.devises, period=fxcm_trading_configuration.period,
                               number=fxcm_trading_configuration.number)
    df['close'] = df[["bidclose", "askclose"]].mean(axis=1)
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
                {'x': forecast['ds'][begin_param:end_param], 'y': forecast['close'][begin_param:end_param], 'type': 'line', 'name': 'Close Price'},
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
    #log_mode_debug()
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
    #scheduler.init_app(app)
    #scheduler.start()
    app.run_server(debug=True)
