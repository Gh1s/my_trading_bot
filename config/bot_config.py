import yaml
import logging


logger = logging.getLogger("Trading-Bot")

yaml_file = open('config/config.yml')
config_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)



class fxcm_connection_config:
    def __init__(self, config_yaml):
        self.token = config_yaml['fxcm']['token']
        self.log_level = config_yaml['fxcm']['log_level']
        self.server_mode = config_yaml['fxcm']['server_mode']
        self.log_file = config_yaml['fxcm']['log_file']


class fxcm_trading_config:
    def __init__(self, config_yaml):
        self.order_amount = config_yaml['fxcm']['order_amount']
        self.devises = config_yaml['fxcm']['devises']
        self.period = config_yaml['fxcm']['period']
        self.number = config_yaml['fxcm']['number']


class prophet_config:
    def __init__(self, config_yaml):
        self.predictions = config_yaml['prophet']['predictions']
        self.changepoint = config_yaml['prophet']['changepoint']


class chart_parameters:
    def __init__(self, config_yaml):
        self.begin = config_yaml['chart']['parameters']['begin']
        self.end = config_yaml['chart']['parameters']['end']


class yahoo_config:
    def __init__(self, config_yaml):
        self.tickers = config_yaml['yfinance']['tickers']
        self.period = config_yaml['yfinance']['period']
        self.interval = config_yaml['yfinance']['interval']


class Scheduler_Config:
    SCHEDULER_API_ENABLED = True


fxcm_connection_configuration = fxcm_connection_config(config_yaml)
fxcm_trading_configuration = fxcm_trading_config(config_yaml)
prophet_configuration = prophet_config(config_yaml)
chart_parameters_config = chart_parameters(config_yaml)
yahoo_config = yahoo_config(config_yaml)
