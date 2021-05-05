import numpy as np
from bot.models.bot_models import Buy_Position, Sell_Position, Closed_Position


def Trading_Analysis(current_price, upper_limit, lower_limit, mean_limit):
    buy_flag = False
    sell_flag = False
    buy_position = {}
    sell_position = {}
    closed_position = {}


    for i in range(1, len(current_price)):

        if current_price[i] > upper_limit[i] and sell_flag == False:

            print("Short the Market")
            sell_flag = True
            buy_position.append(np.nan)
            sell_position.append(current_price[i])
            closed_position.append(np.nan)


        elif current_price[i] < lower_limit[i] and buy_flag == False:

            print("Buy Buy Buy")
            buy_flag = True
            buy_position.append(current_price[i])
            sell_position.append(np.nan)
            closed_position.append(np.nan)


        elif sell_flag == True and current_price[i] <= mean_limit[i]:

            print("Close the short position")
            sell_flag = False
            buy_position.append(np.nan)
            sell_position.append(np.nan)
            closed_position.append(current_price[i])


        elif buy_flag == True and current_price[i] >= mean_limit[i]:

            print("Close the buy position")
            buy_flag = False
            buy_position.append(np.nan)
            sell_position.append(np.nan)
            closed_position.append(current_price[i])

        else:
            buy_position.append(np.nan)
            sell_position.append(np.nan)
            closed_position.append(np.nan)

    return buy_position, sell_position, closed_position