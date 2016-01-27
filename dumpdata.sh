TIMESTAMP=`date +%s`

./manage.py dumpdata --indent=2 \
	checklist auth.User sessions sites socialaccount | \
	tee ~/dump.$TIMESTAMP.json
