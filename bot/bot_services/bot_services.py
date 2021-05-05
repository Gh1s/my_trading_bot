from config.bot_config import config_yaml
import logging


def log_mode_debug():
    if config_yaml['debug_log']:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s [%(levelname)s] %(name)-12s - %(message)s",
                            handlers=[logging.StreamHandler()])
    else:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s [%(levelname)s] %(name)-12 - %(message)s",
                            handlers=[logging.StreamHandler()])


def display_logs(print_msg, log_msg):
    print(print_msg)
    logging.info(log_msg)