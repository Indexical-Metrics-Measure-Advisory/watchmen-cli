FROM python:3.9

WORKDIR /app
ADD . .
RUN pip install requests
RUN pip install fire

ENV path="/app", host="http://0.0.0.0:8000" username="imma-admin" password="abc123"
CMD python cli.py deploy --path_=$path --host=$host --username=$username --password=$password
