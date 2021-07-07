FROM python:3.9

WORKDIR /app
ADD . .
RUN pip install requests
RUN pip install fire

ENV path="/app", host=0.0.0.0 port=8000 username="imma-admin" password="abc123"
CMD ["python","cli.py","deploy", "--path_=$path", "--host=$host", "--port=$port", "--username=$username", "--password=$password"]






