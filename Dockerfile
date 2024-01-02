# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.9-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.9

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY netbird /bin/netbird

RUN chmod +x /bin/netbird

COPY command.sh /command.sh

RUN chmod +x /command.sh

CMD /command.sh

ENV NB_USE_NETSTACK_MODE=true \
  NB_SOCKS5_LISTENER_PORT=1080 \
  NB_FOREGROUND_MODE=true \
  NB_LOG_LEVEL=debug

# index root directory
ENV AzureWebJobsFeatureFlags=EnableWorkerIndexing

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY function_app.py /home/site/wwwroot/
COPY host.json /home/site/wwwroot/