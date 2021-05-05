from python
WORKDIR /my_trading_bot
COPY requirements.txt requirements.txt
COPY analysis_and_prediction/* analysis_and_prediction/
COPY bot/* bot/
COPY config/* config/
RUN pip install -r requirements.txt
EXPOSE 8050
RUN python /my_trading_bot/analysis_and_prediction/display_chart.py