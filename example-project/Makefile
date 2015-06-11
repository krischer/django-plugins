.PHONY: all
all: bin/python db.sqlite3

bin/python:
	virtualenv --no-site-packages .
	cd .. && $(CURDIR)/bin/python setup.py develop

db.sqlite3:
	bin/python manage.py migrate

.PHONY: run
run:
	bin/python manage.py runserver


.PHONY: clean
clean:
	rm -rf bin build var
	find -type f -iname '*.pyc' -exec rm {} +
