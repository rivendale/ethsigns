#!/bin/bash

echo "<<<<<<<<<<<<<<<<<<<< START APP >>>>>>>>>>>>>>>>>>>>>>>>"
# Start the API with gunicorn
gunicorn --access-logfile '-' --workers 2 -t 3600 ethsigns:app -b 0.0.0.0:5000
