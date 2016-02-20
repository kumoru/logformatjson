.PHONY: lint
lint:
	pylint logformatjson tests/*.py

.PHONY: test
test:
	PYTHONPATH=. py.test --cov-report term-missing --cov=logformatjson -vv

.PHONY: circle-test
circle-test:
	py.test -v tests/
