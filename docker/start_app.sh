#!/bin/bash

sleep 10
echo "<<<<<<<< Database Setup and Migrations Starts >>>>>>>>>"
# Run database migrations
flask db upgrade head &

echo " "
echo " "

echo "<<<<<<< Database Setup and Migrations Complete >>>>>>>>>>"
sleep 5
echo " "

echo " "
echo "<<<<<<<<<<<<<<<<<<<< START Celery Worker >>>>>>>>>>>>>>>>>>>>>>"

# # start Celery worker
celery -A celery_worker.celery_app worker --loglevel=info &

echo " "

echo " "
echo "<<<<<<<<<<<<<<<<<<<< START Celery Beat>>>>>>>>>>>>>>>>>>>>>>"
# start celery beat
celery -A celery_conf.celery_periodic_scheduler beat --loglevel=info -s /tmp/celerybeat-schedule &

echo " "

echo ""
echo "<<<<<<<<<<<<<<<<<<<< START APP >>>>>>>>>>>>>>>>>>>>>>>>"
# Start the API with gunicorn
gunicorn --access-logfile '-' --workers 2 -t 3600 ethsigns:app -b 0.0.0.0:5000
