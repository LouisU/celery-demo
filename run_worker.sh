#!/usr/bin/env bash
sleep 5

cd /var/www/celery-demo
celery -A ned.celery.instance worker -l INFO