#!/bin/bash

echo "<<<<<<<< Database Setup and Migrations Starts >>>>>>>>>"
# Run database migrations
flask db upgrade head &&

sleep 2
echo "<<<<<<< Database Setup and Migrations Complete >>>>>>>>>>"
echo " "

echo ""
echo "<<<<<<<<<<<<<<<<<<<< START APP >>>>>>>>>>>>>>>>>>>>>>>>"
# Start the API with gunicorn
gunicorn --access-logfile '-' --workers 2 -t 3600 ethsigns:app -b 0.0.0.0:5000
