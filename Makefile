HTMLCOV_DIR ?= htmlcov

install-dependencies:
	pip install --no-cache-dir -r listener/requirements.txt
	pip install --no-cache-dir -r logger/requirements.txt

# test

coverage-html:
	coverage html -d $(HTMLCOV_DIR) --fail-under 100

coverage-report:
	coverage report -m

test:
	flake8 --ignore=ANN101,ANN201,ANN001,ANN204 listener logger
	coverage run -m pytest gateway/test $(ARGS)
	coverage run --append -m pytest listener/test $(ARGS)
	coverage run --append -m pytest logger/test $(ARGS)

coverage: test coverage-report coverage-html