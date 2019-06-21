#!/usr/bin/env bash
sleep 5

cd /var/www/celery-demo
celery -A nedcelery.celery.celery worker -l info