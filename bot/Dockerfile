FROM continuumio/miniconda3
WORKDIR /my_trading_bot
COPY analysis_and_prediction/* analysis_and_prediction/
COPY analysis_and_prediction/analysis_services/* analysis_and_prediction/analysis_services/
COPY bot/* bot/
COPY bot/bot_services/* bot/bot_services/
COPY config/* config/
ENV PYTHONPATH /my_trading_bot
RUN conda install python=3.9
RUN pip install --upgrade pip
#RUN conda install -c conda-forge pystan==2.19.1.1
RUN conda install -c conda-forge prophet
#RUN conda install -c conda-forge dash
RUN pip install -U fxcmpy
RUN conda install -c anaconda pyyaml
RUN conda install -c conda-forge python-socketio==5.0.4
RUN pip install python-engineio==3.9
RUN conda install -c conda-forge elasticsearch

CMD [ "python", "bot/main.py" ]