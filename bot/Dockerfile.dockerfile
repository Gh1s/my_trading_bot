FROM python:alpine
WORKDIR /my_trading_bot/
COPY /my_trading_bot/*py /my_trading_bot/
COPY /my_trading_bot/bot/requirements.txt /my_trading_bot/bot/requirements.txt
COPY /my_trading_bot/analysis_and_prediction/*py /my_trading_bot/analysis_and_prediction/
COPY /my_trading_bot/bot/*py /my_trading_bot/bot/
COPY /my_trading_bot/config/*py /my_trading_bot/config/
RUN pip install --upgrade pip
RUN pip install -U -r /my_trading_bot/bot/requirements.txt
EXPOSE 8050
CMD [ "python", "bot/main.py" ]