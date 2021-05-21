from config.bot_config import fxcm_trading_configuration, fxcm_connection_configuration
import fxcmpy
from config.bot_config import fxcm_connection_config, fxcm_trading_config, config_yaml, logger


fxcm_connection_configuration = fxcm_connection_config(config_yaml)
fxcm_trading_configuration = fxcm_trading_config(config_yaml)


def TradingOrder(upper_limit, lower_limit, mean_limit, close):
    logger.info("##############################  Trading Bot started  ##############################")


    con = fxcmpy.fxcmpy(access_token=fxcm_connection_configuration.token,
                        log_level="error",
                        server=fxcm_connection_configuration.server_mode,
                        log_file=fxcm_connection_configuration.log_file)

    logger.info("############################## Connected to FXCM  ##############################")
    con.subscribe_market_data(fxcm_trading_configuration.devises)
    #price = con.get_last_price(fxcm_trading_configuration.devises)
    #current_price_bid = price.Bid
    #current_price_ask = price.Ask
    tradePosition = con.get_open_positions().T

    logger.info("#######   Check if a position is open  ########")
    if tradePosition.empty is True:
        logger.info("#######   No open position check if price > upper limit or < lower limit  ########")
        if close > upper_limit:
            logger.info("############  Current price > upper limit => Short Short Short  ################")
            con.create_market_sell_order(fxcm_trading_configuration.devises,
                                     fxcm_trading_configuration.order_amount)

        elif close < lower_limit:
            logger.info("############  Current price < lower limit => Buy Buy Buy  ################")
            con.create_market_buy_order(fxcm_trading_configuration.devises,
                                        fxcm_trading_configuration.order_amount)

        else:
            logger.info("############  No opportunity for the moment => Stand By Position  ################")


    elif tradePosition.empty is not True:
        if tradePosition[0][15] == True:
            logger.info("############  We have a current buy open position  ################")
            if close >= mean_limit:
                logger.info("############  Close the current buy position  ################")
                con.close_all_for_symbol(fxcm_trading_configuration.devises)
            else:
                logger.info("############  Close price not reached stay in the current buy position  ################")

        elif tradePosition[0][15] == False:
            logger.info("############  We have a current sell open position  ################")
            if close <= mean_limit:
                logger.warning("############  Close the current sell position  ################")
                con.close_all_for_symbol(fxcm_trading_configuration.devises)
            else:
                logger.info("############  Close price not reached stay in the current sell position  ################")


    else:
        logger.info("############  No opportunity for the moment => Stand By Position  ################")
