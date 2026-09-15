setup:
	python3 -m venv venv || true
	. venv/bin/activate && pip install -r requirements.txt
	./venv/bin/playwright install
	

test: setup
	. venv/bin/activate && pytest suites/ -v --junitxml=result.xml