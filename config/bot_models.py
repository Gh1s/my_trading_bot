import yaml
import logging


logger = logging.getLogger("Trading-Bot")


class Fxcm_Connection_Config:
    def __init__(self, config_yaml):
        self.token = config_yaml['fxcm']['token']
        self.log_level = config_yaml['fxcm']['log_level']
        self.server_mode = config_yaml['fxcm']['server_mode']
        self.log_file = config_yaml['fxcm']['log_file']


class Fxcm_Trading_Config:
    def __init__(self, config_yaml):
        self.order_amount = config_yaml['fxcm']['order_amount']
        self.mean_close_amount = config_yaml['fxcm']['mean_close_amount']
        self.devises = config_yaml['fxcm']['devises']
        self.period = config_yaml['fxcm']['period']
        self.number = config_yaml['fxcm']['number']


class Prophet_Config:
    def __init__(self, config_yaml):
        self.predictions = config_yaml['prophet']['predictions']
        self.changepoint = config_yaml['prophet']['changepoint']


class Chart_Parameters:
    def __init__(self, config_yaml):
        self.begin = config_yaml['chart']['parameters']['begin'] if 'begin' in config_yaml['chart']['parameters'].keys() else None
        self.end = config_yaml['chart']['parameters']['end'] if 'end' in config_yaml['chart']['parameters'].keys() else None


class Scheduler_Config:
    SCHEDULER_API_ENABLED = True


class Debug_Config:
    def __init__(self, config_yaml):
        self.debug = config_yaml['debug_log']