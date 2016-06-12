#!/bin/bash

NAME="personal_website_django"                                  # Name of the application
DJANGODIR=/home/pi/web/personal_website_django             # Django project directory
SOCKFILE=/home/pi/web/run/gunicorn.sock  # we will communicte using this unix socket
# USER=hello                                        # the user to run as
# GROUP=webapps                                     # the group to run as
NUM_WORKERS=9                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=personal_website_django.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=personal_website_django.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
# cd $DJANGODIR
# source ../bin/activate
# export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=unix:$SOCKFILE \
