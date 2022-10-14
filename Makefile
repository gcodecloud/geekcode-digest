SHELL = /bin/bash
init:
	pip3 install -r requirements.txt

start:
	cd src && python3 sync.py

.PYONY: start-create
start-create: init
	cd src && python3 create_digest_md.py

.PYONY: init start