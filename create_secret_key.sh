#!/bin/bash

rm -rf /tmp/dummy

(cd /tmp && django-admin startproject dummy)

grep SECRET_KEY /tmp/dummy/dummy/settings.py >> private_stuff.py
