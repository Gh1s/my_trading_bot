import yaml
import logging


yaml_file = open('config/config.yml')
config_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
logger = logging.getLogger("Trading-Bot")


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


class yahoo_config:
    def __init__(self, config_yaml):
        self.tickers = config_yaml['yahoo_finance']['tickers']
        self.period = config_yaml['yahoo_finance']['period']
        self.interval = config_yaml['yahoo_finance']['interval']
        self.group_by = config_yaml['yahoo_finance']['group_by']
        self.auto_adjust = config_yaml['yahoo_finance']['auto_adjust']
        self.threads = config_yaml['yahoo_finance']['threads']
        self.proxy = config_yaml['yahoo_finance']['proxy']


class prophet_config:
    def __init__(self, config_yaml):
        self.predictions = config_yaml['prophet']['predictions']


class chart_parameters:
    def __init__(self, config_yaml):
        self.begin = config_yaml['chart']['parameters']['begin']
        self.end = config_yaml['chart']['parameters']['end']


class Scheduler_Config:
    SCHEDULER_API_ENABLED = True


yahoo_configuration = yahoo_config(config_yaml)
fxcm_connection_configuration = fxcm_connection_config(config_yaml)
fxcm_trading_configuration = fxcm_trading_config(config_yaml)
prophet_configuration = prophet_config(config_yaml)
chart_parameters_config = chart_parameters(config_yaml)
