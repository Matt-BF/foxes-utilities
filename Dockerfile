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

# install numpy dependencies otherwise piwheels crashes
RUN apt-get update && apt-get install -y libgfortran5 libatlas3-base cron libxslt1.1 libreoffice
RUN export LC_ALL=en_US.UTF-8

#Copy files to image and set new workdir
ADD . /app
#set new workdir
WORKDIR /app

# make gunicorn boot executable
RUN chmod +x boot.sh

# Using pip and pywheels(RPi):
RUN python3 -m pip install -r requirements.txt --timeout 10000 --extra-index-url https://www.piwheels.org/simple

#Install Gunicorn
RUN pip install gunicorn

ENV FLASK_APP=./run.py

#Change debug to real path
RUN sed -i "s/debug=True/host='0.0.0.0', port=8080/" run.py

#Port to expose
EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
