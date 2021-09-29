from analysis_and_prediction.analysis_services.bot_analysis import prediction, sell_analysis, buy_analysis, \
    dataframe_list_to_decimal, trend_analysis_sell, trend_analysis_buy, close_position
from config.bot_config import fxcm_trading_configuration
from config.bot_config import logger


def TradingOrder(connexion, devises):
    logger.info("##############################  Trading Bot started  ##############################")

    df = connexion.get_candles(devises, period=fxcm_trading_configuration.period,
                               number=fxcm_trading_configuration.number)
    df['close'] = df[["bidclose", "askclose"]].mean(axis=1)
    df.index = df.index.strftime('%Y/%m/%d %H:%M:%S')
    forecast = prediction(df)
    mean_limit = float(forecast['yhat'].iloc[-2:-1])
    mean_limit = '{0:.6f}'.format(mean_limit)
    close = float(forecast['close'].iloc[-2:-1])
    close = '{0:.6f}'.format(close)
    trend = forecast['trend'].iloc[-6:-1]
    trend = dataframe_list_to_decimal(trend)
    sell_position = sell_analysis(forecast)
    buy_position = buy_analysis(forecast)
    close_list = close_position(forecast)

    tradePosition = connexion.get_open_positions().T

    logger.info("#######   {0}  ########".format(devises))
    logger.info("#######   Check if a position is open  ########")
    if tradePosition.empty is True:
        logger.info("#######   No open position check if price > upper limit or < lower limit  ########")
        if -1 in sell_position and trend_analysis_sell(trend) == 'SELL':
            logger.info("############  Current price > upper limit => Short Short Short  ################")
            connexion.create_market_sell_order(devises, fxcm_trading_configuration.order_amount)
            logger.info("############  Get open position information down below  ################")
            connexion.get_open_positions().T
            deconnexion(forecast, sell_position, buy_position, trend, close_list)

        elif -1 in buy_position and trend_analysis_buy(trend) == 'BUY':
            logger.info("############  Current price < lower limit => Buy Buy Buy  ################")
            connexion.create_market_buy_order(devises, fxcm_trading_configuration.order_amount)
            logger.info("############  Get open position information down below  ################")
            connexion.get_open_positions().T
            deconnexion(forecast, sell_position, buy_position, trend, close_list)

        else:
            logger.info("############  No opportunity for the moment => Stand By Position  ################")
            deconnexion(forecast, sell_position, buy_position, trend, close_list)


    elif tradePosition.iloc[14] is True and tradePosition.iloc[13] == devises:

        logger.info(
            "############  We have a current buy open position for the following devise: {0}  ################"
                .format(devises))
        if 1 in close_list or 1 in sell_position:
            logger.info("############  Close the current buy position  ################")
            connexion.close_all_for_symbol(devises)
            logger.info("############  Get closed position information down below  ################")
            connexion.get_closed_positions().T
            deconnexion(forecast, sell_position, buy_position, trend, close_list)
        else:
            logger.info(
                "############  Close price not reached stay in the current buy position  ################")
            deconnexion(forecast, sell_position, buy_position, trend, close_list)

    elif not tradePosition.iloc[14] and tradePosition.iloc[13] == devises:
        logger.info("############  We have a current sell open position  ################")
        if -1 in close_list or 1 in buy_position:
            logger.info("############  Close the current sell position  ################")
            connexion.close_all_for_symbol(devises)
            logger.info("############  Get closed position information down below  ################")
            connexion.get_closed_positions().T
            deconnexion(forecast, sell_position, buy_position, trend, close_list)
        else:
            logger.info(
                "############  Close price not reached stay in the current sell position  ################")
            deconnexion(forecast, sell_position, buy_position, trend, close_list)

    else:
        logger.info("############  No opportunity for the moment => Stand By Position  ################")
        deconnexion(forecast, sell_position, buy_position, trend, close_list)


def deconnexion(forecast, sell_position, buy_position, trend, close_position):
    logger.info("############  Déconnexion  ################")
    # connexion.close()
    yhat_upper = float(forecast['yhat_upper'].iloc[-2:-1])
    yhat_upper = '{0:.6f}'.format(yhat_upper)
    yhat_lower = float(forecast['yhat_lower'].iloc[-2:-1])
    yhat_lower = '{0:.6f}'.format(yhat_lower)
    yhat = float(forecast['yhat'].iloc[-2:-1])
    yhat = '{0:.6f}'.format(yhat)
    close = float(forecast['close'].iloc[-2:-1])
    close = '{0:.6f}'.format(close)
    trend = trend
    close_position = close_position
    logger.info("##############   Price: " + str(close) + "  ##############")
    logger.info("##############   yhat_upper: " + str(yhat_upper) + "  ##############")
    logger.info("##############  yhat_med: " + str(yhat) + "  ##############")
    logger.info("##############   yhat_lower: " + str(yhat_lower) + "  ##############")
    logger.info("##############   sell_position: " + str(sell_position) + "  ##############")
    logger.info("##############   buy_position: " + str(buy_position) + "  ##############")
    logger.info("##############   trend: " + str(trend) + "  ##############")
    logger.info("##############   close_position: " + str(close_position) + "  ##############")
