init:
	pip install -r requirements.txt

setup:
	mkdir ~/.s3medul
	cp ./config.json ~/.s3medul/config.json
	python ./mime_update.py


venv:
	source .venv/bin/activate
