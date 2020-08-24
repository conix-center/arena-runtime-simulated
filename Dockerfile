FROM python:3
RUN apt-get update
RUN apt-get install -y wget mosquitto-clients
RUN pip install --upgrade pip
RUN pip install virtualenv

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD python main.py 

EXPOSE 5000