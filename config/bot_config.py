import  yaml
from models.bot_models import *


yaml_file = open('config/config.yml')
config_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)

def fxcm_connection_config():
    token = config_yaml['fxcm']['token']
    log_level = config_yaml['fxcm']['log_level']
    server_mode = config_yaml['fxcm']['server_mode']
    log_file = config_yaml['fxcm']['log_file']
    fxcm_connection = FXCM_Connection_Model(token, log_level, server_mode, log_file)
    return fxcm_connection

def fxcm_trading_config():
    order_amount = config_yaml['fxcm']['order_amount']
    devises = config_yaml['fxcm']['devises']
    fxcm_trading = FXCM_Trading_Model(order_amount, devises)
    return fxcm_trading

def yahoo_config():
    tickers = config_yaml['yahoo_finance']['tickers']
    period = config_yaml['yahoo_finance']['period']
    interval = config_yaml['yahoo_finance']['interval']
    group_by = config_yaml['yahoo_finance']['group_by']
    auto_adjust = config_yaml['yahoo_finance']['auto_adjust']
    threads = config_yaml['yahoo_finance']['threads']
    proxy = config_yaml['yahoo_finance']['proxy']
    yahoo = Yahoo_Model(tickers, period, interval, group_by, auto_adjust, threads, proxy)
    return yahoo

def prophet_config():
    predictions = config_yaml['prophet']['predictions']
    prophet = Prophet_Model(predictions)
    return prophet
