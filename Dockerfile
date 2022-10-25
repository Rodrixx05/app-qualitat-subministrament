FROM python:3.8.6-slim-buster

LABEL maintainer "Marc Rodriguez, marc.rodri5@gmail.com"

# set working directory in container
WORKDIR /usr/src/app

# Copy and install packages
COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt

# Copy app folder to app folder in container
COPY /app /usr/src/app/

EXPOSE 8080

CMD ["gunicorn", "--workers", "3", "--threads", "1", "-b", "0.0.0.0:8080", "app:server"]