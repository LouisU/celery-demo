FROM python:3.7.3

# work directory
COPY . /var/www/celery-demo
WORKDIR /var/www/celery-demo

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod 755 run_beat.sh && chmod 755 run_worker.sh && chmod 755 run_web.sh

EXPOSE 5000
