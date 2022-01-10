import logging
import os
import yaml
from config.bot_models import Fxcm_Trading_Config, Fxcm_Connection_Config, Prophet_Config, Chart_Parameters, Debug_Config

logger = logging.getLogger('configuration')


class Config:
    # Singleton
    __instance = None
    config_yaml = None
    fxcm_trading_config = None
    fxcm_connection_config = None
    prophet_config = None
    chart_parameters = None
    debug_conf = None

    # Singleton
    def __new__(cls):
        if Config.__instance is None:
            print("#Config# : new configuration")
            Config.__instance = object.__new__(cls)
            print("#Config# : __init__")
            Config.__instance.read_config_file()
            Config.__instance.override_with_os_variable()
            Config.__instance.apply_config()
            print("#Config# : EO __init__")
        return Config.__instance


    def read_config_file(self):
        print("#Config# : read_config_file")
        yaml_file = open('config/config.yml')
        self.config_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)

    def apply_config(self):
        print("#Config# : apply_config")
        logger.info("extracting config to class")
        if self.config_yaml['debug_log']:
            logging.basicConfig(level=logging.DEBUG,
                                format="%(asctime)s [%(levelname)s] %(name)-12s - %(message)s",
                                handlers=[logging.StreamHandler()])
        else:
            logging.basicConfig(level=logging.INFO,
                                format="%(asctime)s [%(levelname)s] %(name)-12 - %(message)s",
                                handlers=[logging.StreamHandler()])

        self.fxcm_connection_config = Fxcm_Connection_Config(self.config_yaml)
        self.fxcm_trading_config = Fxcm_Trading_Config(self.config_yaml)
        self.prophet_config = Prophet_Config(self.config_yaml)
        self.chart_parameters = Chart_Parameters(self.config_yaml)

    def override_with_os_variable(self):
        print("#Config# : override_with_os_variable")
        # Surcharge par variable d'environnement
        self.config_yaml['fxcm']['order_amount'] = os.getenv('ORDER_AMOUNT', self.config_yaml['fxcm']['order_amount'])
        self.config_yaml['fxcm']['devises'] = os.getenv('DEVISES', self.config_yaml['fxcm']['devises'])
        self.config_yaml['fxcm']['period'] = os.getenv('PERIOD', self.config_yaml['fxcm']['period'])
        self.config_yaml['fxcm']['number'] = os.getenv('NUMBER', self.config_yaml['fxcm']['number'])

