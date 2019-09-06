FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
apt-get install git

COPY . .
WORKDIR /usr/src/app
CMD [ "python", "./modules/main.py" ]