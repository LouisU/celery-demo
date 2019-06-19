FROM python:3.7.3

# work directory
COPY . /var/www/celery-demo
WORKDIR /var/www/celery-demo

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
