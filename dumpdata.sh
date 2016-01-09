TIMESTAMP=`date +%s`

./manage.py dumpdata --indent=2 \
	checklist auth.User sessions | \
	tee ~/dump.$TIMESTAMP.json
