SHELL = /bin/bash
init:
	pip3 install -r requirements.txt
start:
	cd src && python3 sync.py
.PYONY: init start