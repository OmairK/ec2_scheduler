#!/bin/bash

# Start Celery Beat
celery -A celery beat --loglevel=DEBUG &> /log/celery_beat.log&

# Start Celery Workers
celery -A celery worker --loglevel=DEBUG