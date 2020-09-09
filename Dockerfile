FROM python:3.7
ADD transfer-name-server.py requirements.txt /
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "./transfer-name-server.py" ]