from models.bot_models import fxcm_trading_configuration, fxcm_connection_configuration
import fxcmpy
import logging
from config.bot_config import fxcm_connection_config, fxcm_trading_config, config_yaml


fxcm_connection_configuration = fxcm_connection_config(config_yaml)
fxcm_trading_configuration = fxcm_trading_config(config_yaml)


def TradingOrder(upper_limit, lower_limit, mean_limit):
    print("################  Trading Bot started  ##############################")
    logging.info("################  Trading Bot started  ##############################")

    try:
        con = fxcmpy.fxcmpy(access_token=fxcm_connection_configuration.token,
                            log_level="error",
                            server=fxcm_connection_configuration.server_mode,
                            log_file=fxcm_connection_configuration.log_file)
    except:
        print("############  Failed to connect to FXCM  ################")
        logging.error("Failed to connect to FXCM")

    con.subscribe_market_data(fxcm_trading_configuration.devises)
    price = con.get_last_price(fxcm_trading_configuration.devises)
    current_price_bid = price.Bid
    current_price_ask = price.Ask
    tradePosition = con.get_open_positions().T

    if tradePosition.empty is True and current_price_ask > upper_limit:
        print("############  Short Short Short  ################")
        logging.info("Short Short Short")
        con.create_market_sell_order(fxcm_trading_configuration.devises,
                                     fxcm_trading_configuration.order_amount)


    elif tradePosition.empty is True and current_price_bid < lower_limit:
        print("############  Buy Buy Buy  ################")
        logging.info("Buy Buy Buy")
        con.create_market_buy_order(fxcm_trading_configuration.devises,
                                    fxcm_trading_configuration.order_amount)


    elif tradePosition.empty is not True and tradePosition[0][15] == True:
        print("############  We have a current buy open position  ################")
        logging.info("We have a current buy open position")
        if current_price_ask >= mean_limit:
            print("############  Close the current buy position  ################")
            logging.info("Close the current buy position")
        else:
            print("############  Close price not reached stay in the current buy position  ################")
            logging.info("Close price not reached stay in the current buy position")


    elif tradePosition.empty is not True and tradePosition[0][15] == False:
        print("############  We have a current sell open position  ################")
        logging.info("We have a current sell open position")
        if current_price_bid <= mean_limit:
            print("############  Close the current sell position  ################")
            logging.info("Close the current sell position")
        else:
            print("############  Close price not reached stay in the current sell position  ################")
            logging.info("Close price not reached stay in the current sell position")


    else:
        print("############  Stand By Position  ################")
        logging.warning("Stand By Position")
