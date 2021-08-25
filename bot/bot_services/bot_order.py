import fxcmpy
from analysis_and_prediction.analysis_services.bot_analysis import prediction, sell_analysis, buy_analysis, \
    get_yahoo_data
from config.bot_config import fxcm_trading_configuration, fxcm_connection_configuration, yahoo_config
from config.bot_config import logger


def TradingOrder():
    logger.info("##############################  Trading Bot started  ##############################")

    df = get_yahoo_data(yahoo_config.tickers)
    df.index = df.index.strftime('%Y/%m/%d %H:%M:%S')
    forecast = prediction(df)

    con = fxcmpy.fxcmpy(access_token=fxcm_connection_configuration.token,
                  log_level="error",
                  server=fxcm_connection_configuration.server_mode,
                  log_file=fxcm_connection_configuration.log_file)

    logger.info("############################## Connected to FXCM  ##############################")
    con.subscribe_market_data(fxcm_trading_configuration.devises)

    mean_limit = float(forecast['yhat'].iloc[-2:-1])
    mean_limit = '{0:.6f}'.format(mean_limit)
    close = float(forecast['close'].iloc[-2:-1])
    close = '{0:.6f}'.format(close)
    trend = float(forecast['trend'].iloc[-2:-1])
    trend = '{0:.6f}'.format(trend)
    sell_position = sell_analysis(forecast)
    buy_position = buy_analysis(forecast)

    tradePosition = con.get_open_positions().T

    logger.info("#######   Check if a position is open  ########")
    if tradePosition.empty is True:
        logger.info("#######   No open position check if price > upper limit or < lower limit  ########")
        if -1 in sell_position and trend < mean_limit:
            logger.info("############  Current price > upper limit => Short Short Short  ################")
            con.create_market_sell_order(fxcm_trading_configuration.devises,
                                         fxcm_trading_configuration.order_amount)
            logger.info("############  Get open position information down below  ################")
            con.get_open_positions().T
            deconnexion(forecast, con, sell_position, buy_position, trend)

        elif -1 in buy_position and trend > mean_limit:
            logger.info("############  Current price < lower limit => Buy Buy Buy  ################")
            con.create_market_buy_order(fxcm_trading_configuration.devises,
                                        fxcm_trading_configuration.order_amount)
            logger.info("############  Get open position information down below  ################")
            con.get_open_positions().T
            deconnexion(forecast, con, sell_position, buy_position, trend)

        else:
            logger.info("############  No opportunity for the moment => Stand By Position  ################")
            deconnexion(forecast, con, sell_position, buy_position, trend)


    elif tradePosition.empty is not True:
        if tradePosition[0][14]:
            logger.info("############  We have a current buy open position  ################")
            if close >= mean_limit or trend < mean_limit:
                logger.info("############  Close the current buy position  ################")
                con.close_all_for_symbol(fxcm_trading_configuration.devises)
                logger.info("############  Get closed position information down below  ################")
                con.get_closed_positions().T
                deconnexion(forecast, con, sell_position, buy_position, trend)
            else:
                logger.info("############  Close price not reached stay in the current buy position  ################")
                deconnexion(forecast, con, sell_position, buy_position, trend)

        elif not tradePosition[0][14]:
            logger.info("############  We have a current sell open position  ################")
            if close <= mean_limit or trend > mean_limit:
                logger.info("############  Close the current sell position  ################")
                con.close_all_for_symbol(fxcm_trading_configuration.devises)
                logger.info("############  Get closed position information down below  ################")
                con.get_closed_positions().T
                deconnexion(forecast, con, sell_position, buy_position, trend)
            else:
                logger.info("############  Close price not reached stay in the current sell position  ################")
                deconnexion(forecast, con, sell_position, buy_position, trend)


        else:
            logger.info("############  We have a problem current position not buy and not sell, please restart the "
                        "Bot  ################")
            deconnexion(forecast, con, sell_position, buy_position, trend)


    else:
        logger.info("############  No opportunity for the moment => Stand By Position  ################")
        deconnexion(forecast, con, sell_position, buy_position, trend)


def deconnexion(forecast, connexion, sell_position, buy_position, trend):
    logger.info("############  Déconnexion  ################")
    connexion.close()
    yhat_upper = float(forecast['yhat_upper'].iloc[-2:-1])
    yhat_upper = '{0:.6f}'.format(yhat_upper)
    yhat_lower = float(forecast['yhat_lower'].iloc[-2:-1])
    yhat_lower = '{0:.6f}'.format(yhat_lower)
    yhat = float(forecast['yhat'].iloc[-2:-1])
    yhat = '{0:.6f}'.format(yhat)
    close = float(forecast['close'].iloc[-2:-1])
    close = '{0:.6f}'.format(close)
    trend = float(forecast['trend'].iloc[-2:-1])
    trend = '{0:.6f}'.format(trend)
    logger.info("##############   Price: " + str(close) + "  ##############")
    logger.info("##############   yhat_upper: " + str(yhat_upper) + "  ##############")
    logger.info("##############  yhat_med: " + str(yhat) + "  ##############")
    logger.info("##############   yhat_lower: " + str(yhat_lower) + "  ##############")
    logger.info("##############   sell_position: " + str(sell_position) + "  ##############")
    logger.info("##############   buy_position: " + str(buy_position) + "  ##############")
    logger.info("##############   trend: " + str(trend) + "  ##############")
