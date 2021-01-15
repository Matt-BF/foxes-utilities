# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.7-buster

# If you prefer miniconda:
# FROM continuumio/miniconda3

LABEL Name=foxes-utilities Version=1


ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

#download and install chrome
RUN apt-get update 
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install


RUN export LC_ALL=en_US.UTF-8

#Copy files to image and set new workdir
ADD . /app
#set new workdir
WORKDIR /app


# make gunicorn boot executable
RUN chmod +x boot.sh

# Using pip and pywheels(RPi):
RUN python3 -m pip install -r requirements.txt --timeout 10000

#Install Gunicorn
RUN pip install gunicorn

ENV FLASK_APP=./run.py

#Change debug to real path
RUN sed -i "s/debug=True/host='0.0.0.0', port=8080/" run.py

#Port to expose
EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
