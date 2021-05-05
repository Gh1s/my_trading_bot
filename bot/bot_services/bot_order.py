from config.bot_config import fxcm_trading_configuration, fxcm_connection_configuration
import fxcmpy
import logging
from config.bot_config import fxcm_connection_config, fxcm_trading_config, config_yaml


fxcm_connection_configuration = fxcm_connection_config(config_yaml)
fxcm_trading_configuration = fxcm_trading_config(config_yaml)


def TradingOrder(upper_limit, lower_limit, mean_limit):
    print("##############################  Trading Bot started  ##############################")
    logging.info("##############################  Trading Bot started  ##############################")


    con = fxcmpy.fxcmpy(access_token=fxcm_connection_configuration.token,
                        log_level="error",
                        server=fxcm_connection_configuration.server_mode,
                        log_file=fxcm_connection_configuration.log_file)

    print("##############################  Connected to FXCM  ##############################")
    logging.info("############################## Connected to FXCM  ##############################")
    con.subscribe_market_data(fxcm_trading_configuration.devises)
    price = con.get_last_price(fxcm_trading_configuration.devises)
    current_price_bid = price.Bid
    current_price_ask = price.Ask
    tradePosition = con.get_open_positions().T

    print("#######   Check if a position is open  ########")
    if tradePosition.empty is True:
        print("#######   No open position check if price > upper limit or < lower limit  ########")
        if current_price_bid > upper_limit:
            print("############  Current price > upper limit => Short Short Short  ################")
            logging.warning("############  Current price > upper limit => Short Short Short  ################")
            con.create_market_sell_order(fxcm_trading_configuration.devises,
                                     fxcm_trading_configuration.order_amount)

        elif current_price_ask < lower_limit:
            print("############  Current price < lower limit => Buy Buy Buy  ################")
            logging.warning("############  Current price < lower limit => Buy Buy Buy  ################")
            con.create_market_buy_order(fxcm_trading_configuration.devises,
                                        fxcm_trading_configuration.order_amount)

        else:
            print("############  No opportunity for the moment => Stand By Position  ################")
            logging.warning("############  No opportunity for the moment => Stand By Position  ################")


    elif tradePosition.empty is not True:
        print("#######   Open Position a that time check if it a buy or a sell position  ########")
        if tradePosition[0][15] == True:
            print("############  We have a current buy open position  ################")
            logging.info("############  We have a current buy open position  ################")
            if current_price_bid >= mean_limit:
                print("############  Close the current buy position  ################")
                logging.warning("############  Close the current buy position  ################")
                con.close_all_for_symbol(fxcm_trading_configuration.devises)
            else:
                print("############  Close price not reached stay in the current buy position  ################")
                logging.info("############  Close price not reached stay in the current buy position  ################")

        elif tradePosition[0][15] == False:
            print("############  We have a current sell open position  ################")
            logging.info("############  We have a current sell open position  ################")
            if current_price_ask <= mean_limit:
                print("############  Close the current sell position  ################")
                logging.warning("############  Close the current sell position  ################")
                con.close_all_for_symbol(fxcm_trading_configuration.devises)
            else:
                print("############  Close price not reached stay in the current sell position  ################")
                logging.info("############  Close price not reached stay in the current sell position  ################")


    else:
        print("############  No opportunity for the moment => Stand By Position  ################")
        logging.warning("############  No opportunity for the moment => Stand By Position  ################")
