FROM python:3.9

WORKDIR /app
ADD . .
RUN pip install requests
RUN pip install fire

ENV path="directory" host="http://0.0.0.0" username="username" password="password"
CMD python cli.py deploy --path_=$path --host=$host --username=$username --password=$password
