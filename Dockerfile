# Dockerfile-flask# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath
FROM python:3.7-stretch
# Set an environment variable with the directory
# where we'll be running the app

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uwsgi", "uwsgi.ini"]