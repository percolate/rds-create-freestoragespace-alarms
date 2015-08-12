develop:
	python setup.py develop

undevelop:
	python setup.py develop --uninstall

test:
	flake8 rds_create_freestoragespace_alarms

clean:
	rm -rf rds-create-freestoragespace-alarms.egg-info/
	rm -rf dist/

release: clean
	python setup.py sdist
	twine upload dist/*
