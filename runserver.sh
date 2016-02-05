#!/bin/bash

IP="$(/sbin/ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{ print $1 }')"

python manage.py runserver $IP:1024 --settings=recurringtasks.settings_debug
