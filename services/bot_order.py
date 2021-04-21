from config.bot_config import fxcm_connection_config, fxcm_trading_config, config_yaml
import fxcmpy
import logging


#sell_flag = False
#buy_flag = False

def DisplayFlag(buy_flag, sell_flag):
    print("buy_flag = " + str(buy_flag))
    print("sell_flag = " + str(sell_flag))


def TradingOrder(upper_limit, lower_limit, mean_limit):


    try:
        con = fxcmpy.fxcmpy(access_token=fxcm_connection_config(config_yaml).token,
                            log_level="error",
                            server=fxcm_connection_config(config_yaml).server_mode,
                            log_file=fxcm_connection_config(config_yaml).log_file)
    except:
        logging.error("Failed to connect to FXCM")

    con.subscribe_market_data(fxcm_trading_config(config_yaml).devises)
    price = con.get_last_price(fxcm_trading_config(config_yaml).devises)
    current_price_bid = price.Bid
    current_price_ask = price.Ask
    tradePosition = con.get_open_positions().T

    if tradePosition.empty is not True:
        if tradePosition[0][15] == True:
            buy_flag = True
            sell_flag = False
            print("We have a current buy position")
            DisplayFlag(buy_flag, sell_flag)
            logging.info("We have a current buy position")
        else:
            buy_flag = False
            sell_flag = True
            DisplayFlag(buy_flag, sell_flag)
            print("We have a current sell position")
            logging.info("We have a current sell position")
    else:
        buy_flag = False
        sell_flag = False
        DisplayFlag(buy_flag, sell_flag)
        print("No current position")
        logging.info("No current position")

    if current_price_ask > upper_limit and sell_flag == False:

        print("Short Short Short")
        logging.info("Short Short Short")
        sell_flag = True
        DisplayFlag(buy_flag, sell_flag)
        con.create_market_sell_order(fxcm_trading_config(config_yaml).devises, fxcm_trading_config(config_yaml).order_amount)

    elif current_price_bid < lower_limit and buy_flag == False:

        print("Buy Buy Buy")
        logging.info("Buy Buy Buy")
        buy_flag = True
        DisplayFlag(buy_flag, sell_flag)
        con.create_market_buy_order(fxcm_trading_config(config_yaml).devises, fxcm_trading_config(config_yaml).order_amount)

    elif sell_flag == True and current_price_bid <= mean_limit:

        print("Close the short position")
        logging.info("Close the short position")
        sell_flag = False
        DisplayFlag(buy_flag, sell_flag)
        con.close_all_for_symbol(fxcm_trading_config(config_yaml).devises)

    elif buy_flag == True and current_price_ask >= mean_limit:

        print("Close the buy position")
        logging.info("Close the buy position")
        buy_flag = False
        DisplayFlag(buy_flag, sell_flag)
        con.close_all_for_symbol(fxcm_trading_config(config_yaml).devises)

    else:
        print("Stand By Position")
        logging.warning("Stand By Position")
        DisplayFlag(buy_flag, sell_flag)

    con.close()