FROM python:3.9

WORKDIR /app
ADD . .
RUN pip install requests
RUN pip install fire

ENV command="deploy" host="http://0.0.0.0" username="username" password="password"
CMD python cli.py $command --host=$host --username=$username --password=$password
