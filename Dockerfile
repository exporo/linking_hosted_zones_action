FROM python:3.7
ADD transfer-name-server.py requirements.txt entrypoint.sh /
RUN pip install -r requirements.txt
ENTRYPOINT ["/entrypoint.sh"]