FROM continuumio/miniconda3
WORKDIR /my_trading_bot
COPY analysis_and_prediction/* analysis_and_prediction/
COPY analysis_and_prediction/analysis_services/* analysis_and_prediction/analysis_services/
COPY bot/* bot/
COPY bot/bot_services/* bot/bot_services/
COPY config/* config/
ENV PYTHONPATH /my_trading_bot
RUN pip install --upgrade pip
RUN conda install -c conda-forge pystan==2.19.1.1
RUN conda install -c conda-forge prophet
#RUN conda install -c conda-forge dash
#RUN conda install -c conda-forge flask-apscheduler
RUN pip install fxcmpy==1.2.6
#RUN pip install yfinance
RUN conda install -c anaconda pyyaml
RUN pip install python-socketio==4.6.1
RUN pip install python-engineio==3.9

CMD [ "python", "bot/main.py" ]