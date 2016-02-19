.PHONY: lint
lint:
	pylint logformatjson tests/*.py

.PHONY: test
test:
	PYTHONPATH=. py.test --cov-report term-missing --cov=logformatjson -vv
