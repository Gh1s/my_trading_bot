from analysis_and_prediction.analysis_services.bot_analysis import dataframe_list_to_decimal, sell_analysis, \
    buy_analysis, close_position, trend_analysis_sell, trend_analysis_buy, prediction
from config.bot_config import logger
from config.bot_config import Config, logger


fxcm_trading_configuration = Config().fxcm_trading_config


def get_instruments():
    liste_instruments = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'AUD/USD', 'USD/CAD']
    return liste_instruments


def Multi_Devises_Strategy(connexion):
    logger.info("##############################  Trading Bot started  ##############################")

    devises = get_instruments()
    for devise in devises:
        logger.info("############  Analysis for the following devises: {0}  ###############"
                    .format(devise))
        df = connexion.get_candles(devise, period=fxcm_trading_configuration.period,
                                   number=fxcm_trading_configuration.number)
        df['close'] = df[["bidclose", "askclose"]].mean(axis=1)
        df.index = df.index.strftime('%Y/%m/%d %H:%M:%S')

        logger.info("##############################  Prophet analysis  ##############################")
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
        logger.info("#######   {0}  ########".format(devise))
        logger.info("#######   Check if a position is open for the {0} devise  ########".format(devise))

        if len(tradePosition.columns) == 0:
            logger.info("#######   No open position for {0} check if price > upper limit or < lower limit  ########"
                        .format(devise))
            if -1 in sell_position and trend_analysis_sell(trend) == 'SELL':
                logger.info("############  Current price > upper limit => Short Short Short  ################")
                # connexion.create_market_sell_order(devises, fxcm_trading_configuration.order_amount)
                #connexion.open_trade(symbol=devise, amount=fxcm_trading_configuration.order_amount, is_buy=False,
                #                     time_in_force="GTC", order_type="AtMarket", is_in_pips=True, limit=15, stop=-50)
                logger.info("############  Get open position information down below  ################")
                connexion.get_open_positions().T

            elif -1 in buy_position and trend_analysis_buy(trend) == 'BUY':
                logger.info("############  Current price < lower limit => Buy Buy Buy  ################")
                # connexion.create_market_buy_order(devises, fxcm_trading_configuration.order_amount)
                #connexion.open_trade(symbol=devise, amount=fxcm_trading_configuration.order_amount, is_buy=True,
                #                     time_in_force="GTC", order_type="AtMarket", is_in_pips=True, limit=15, stop=-50)
                logger.info("############  Get open position information down below  ################")
                connexion.get_open_positions().T

            else:
                logger.info("############  No opportunity for the moment => Stand By Position  ################")

        elif len(tradePosition.columns) != 0:
            logger.info("We have some open positions control if we have one for {0}".format(devise))
            list_open_devises = check_open_devise(tradePosition)
            if devise not in list_open_devises:

                logger.info("We have open positions in FXCM but not for {0}".format(devise))
                if -1 in sell_position and trend_analysis_sell(trend) == 'SELL':
                    logger.info("############  Current price > upper limit => Short Short Short {0}  ################"
                                .format(devise))
                    connexion.open_trade(symbol=devise, amount=fxcm_trading_configuration.order_amount, is_buy=False,
                                         time_in_force="GTC", order_type="AtMarket", is_in_pips=True, limit=15,
                                         stop=-50)
                    logger.info("############  Get open position information down below  ################")
                    connexion.get_open_positions().T

                elif -1 in buy_position and trend_analysis_buy(trend) == 'BUY':
                    logger.info("############  Current price < lower limit => Buy Buy Buy {0}  ################"
                                .format(devise))
                    connexion.open_trade(symbol=devise, amount=fxcm_trading_configuration.order_amount, is_buy=True,
                                         time_in_force="GTC", order_type="AtMarket", is_in_pips=True, limit=15,
                                         stop=-50)
                    logger.info("############  Get open position information down below  ################")
                    connexion.get_open_positions().T

                else:
                    logger.info("############  No opportunity for the moment => Stand By Position {0}  ################"
                                .format(devise))

            elif devise in list_open_devises:
                index_devises = list_open_devises.index(devise)
                if tradePosition[index_devises][13] == devise:

                    logger.info(
                        "############  We have a current buy open position for the following devise: {0}  ################".format(
                            devise))

                else:
                    logger.info("############  No opportunity for the moment => Stand By Position  ################")
            else:
                logger.warn("############   Check eth bot please maybe we have a problem  ################")
        else:
            logger.warn("############   Check eth bot please maybe we have a problem   ################")


    return forecast, sell_position, buy_position, trend, close_list


def deconnexion(forecast, sell_position, buy_position, trend, close_position):
    logger.info("############  Trading position status  ################")
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
    logger.info("##############   We have open positions for those devises {0}  ##############".format(list_open_devises))
    return list_open_devises
