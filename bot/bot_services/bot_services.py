from config.bot_config import Config, logger

fxcm_trading_configuration = Config().fxcm_trading_config


def deconnexion(devise, forecast, sell_position, buy_position, trend, close_position):
    logger.info("############  Trading position status  ################")
    logger.info("Status for the following devise: {0}".format(devise))
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


def check_open_devise(tradePosition):
    list_open_devises = []
    for elem in tradePosition.iloc[13]:
        list_open_devises.append(elem)
    logger.info(
        "##############   We have open positions for those devises {0}  ##############".format(list_open_devises))
    return list_open_devises
