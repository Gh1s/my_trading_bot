class FXCM_Connection_Model(object):
    def __init__(self, token, log_level, server_mode, log_file):
        self.token = token
        self.log_level = log_level
        self.server_mode = server_mode
        self.log_file = log_file

class FXCM_Trading_Model(object):
    def __init__(self, order_amount, devises):
        self.order_amount = order_amount
        self.devises = devises

class Yahoo_Model(object):
    def __init__(self, tickers, period, interval, group_by, auto_adjust, threads, proxy):
        self.tickers = tickers
        self.period = period
        self.interval = interval
        self.group_by = group_by
        self.auto_ajust = auto_adjust
        self.threads = threads
        self.proxy = proxy


class Prophet_Model(object):
    def __init__(self, predictions):
        self.predictions = predictions


# class Models_Encoder(JSONEncoder):
#     def default(self, o):
#         return o.__dict__