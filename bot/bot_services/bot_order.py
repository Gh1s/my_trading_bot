from analysis_and_prediction.analysis_services.bot_analysis import prediction, sell_analysis, buy_analysis, \
    dataframe_list_to_decimal, trend_analysis_sell, trend_analysis_buy, close_position
from bot.bot_services.bot_services import check_open_devise
from config.bot_config import Config, logger
from bot.bot_services.bot_services import deconnexion


fxcm_trading_configuration = Config().fxcm_trading_config


def TradingOrder(connexion, devises):
    for devise in devises:
        logger.info("############  Analysis for the following devises: {0}  ###############"
                    .format(devise))
        logger.info("############  Get the data ###############")
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
                connexion.open_trade(symbol=devise, amount=fxcm_trading_configuration.order_amount, is_buy=False,
                                     time_in_force="GTC", order_type="AtMarket", is_in_pips=True)
                logger.info("############  Get open position information down below  ################")
                connexion.get_open_positions().T
                deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)

            elif -1 in buy_position and trend_analysis_buy(trend) == 'BUY':
                logger.info("############  Current price < lower limit => Buy Buy Buy  ################")
                connexion.open_trade(symbol=devise, amount=fxcm_trading_configuration.order_amount, is_buy=True,
                                     time_in_force="GTC", order_type="AtMarket", is_in_pips=True)
                logger.info("############  Get open position information down below  ################")
                connexion.get_open_positions().T
                deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)

            else:
                logger.info("############  No opportunity for the moment => Stand By Position  ################")
                deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)

        elif len(tradePosition.columns) != 0:
            logger.info("We have some open positions control if we have one for {0}".format(devise))
            list_open_devises = check_open_devise(tradePosition)

            if devise not in list_open_devises:

                logger.info("We have open positions in FXCM but not for {0}".format(devise))
                if -1 in sell_position and trend_analysis_sell(trend) == 'SELL':
                    logger.info("############  Current price > upper limit => Short Short Short {0}  ################"
                                .format(devise))
                    connexion.open_trade(symbol=devise, amount=fxcm_trading_configuration.order_amount, is_buy=False,
                                         time_in_force="GTC", order_type="AtMarket", is_in_pips=True)
                    logger.info("############  Get open position information down below  ################")
                    connexion.get_open_positions().T
                    deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)

                elif -1 in buy_position and trend_analysis_buy(trend) == 'BUY':
                    logger.info("############  Current price < lower limit => Buy Buy Buy {0}  ################"
                                .format(devise))
                    connexion.open_trade(symbol=devise, amount=fxcm_trading_configuration.order_amount, is_buy=True,
                                         time_in_force="GTC", order_type="AtMarket", is_in_pips=True)
                    logger.info("############  Get open position information down below  ################")
                    connexion.get_open_positions().T
                    deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)

                else:
                    logger.info("############  No opportunity for the moment => Stand By Position {0}  ################"
                                .format(devise))
                    deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)

            elif devise in list_open_devises:
                index_devises = list_open_devises.index(devise)
                if tradePosition[index_devises][14] is True and tradePosition[index_devises][13] == devise:
                    logger.info(
                        "############  We have a current buy open position for the following devise: {0}  ################".format(
                            devise))
                    if 1 in sell_position:
                        logger.info("############  Close the current buy position  ################")
                        connexion.close_all_for_symbol(devise)
                        logger.info("############  Get closed position information down below  ################")
                        connexion.get_closed_positions().T
                        deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)
                    else:
                        logger.info(
                            "############  Close price not reached stay in the current buy position  ################")
                        deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)

                elif not tradePosition[index_devises][14] and tradePosition[index_devises][13] == devise:
                    logger.info("############  We have a current sell open position  ################")
                    if 1 in buy_position:
                        logger.info("############  Close the current sell position  ################")
                        connexion.close_all_for_symbol(devise)
                        logger.info("############  Get closed position information down below  ################")
                        connexion.get_closed_positions().T
                        deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)
                    else:
                        logger.info(
                            "############  Close price not reached stay in the current sell position  ################")
                        deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)
                else:
                    logger.info("############  No opportunity for the moment => Stand By Position  ################")
                    deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)
            else:
                logger.warn("############   We have an error   ################")
                deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)
        else:
            logger.warn("############   We have an error   ################")
            deconnexion(devise, forecast, sell_position, buy_position, trend, close_list)


    return forecast, sell_position, buy_position, trend, close_list

