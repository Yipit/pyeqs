# Variables you might need to change in the first place
#
# This is probably the only section you'll need to change in this Makefile.
# Also, make sure you don't remove the `<variables/>' tag. Cause those marks
# are going to be used to update this file automatically.
#
# <variables>
PACKAGE=pyeqs
CUSTOM_PIP_INDEX=pypi
# </variables>

all: unit functional

unit:
	@make run_test suite=unit

functional:
	@make run_test suite=functional

prepare: clean install_deps

run_test:
	@if [ -d tests/$(suite) ]; then \
		echo "Running \033[0;32m$(suite)\033[0m test suite"; \
		make prepare && \
			nosetests --stop --with-coverage --cover-package=$(PACKAGE) \
				--cover-branches --cover-min-percentage=100 --cover-erase --verbosity=2 -s tests/$(suite) ; \
	fi

install_deps:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You're not running this from a virtualenv, wtf?"; \
		exit 1; \
	fi

	@if [ -z $$SKIP_DEPS ]; then \
		echo "Installing missing dependencies..."; \
		[ -e development.txt  ] && pip install -r development.txt --quiet; \
	fi

	@python setup.py develop &> .build.log

clean:
	@echo "Removing garbage..."
	@find . -name '*.pyc' -delete
	@find . -name '*.so' -delete
	@find . -name __pycache__ -delete
	@rm -rf .coverage *.egg-info *.log build dist MANIFEST htmlcov

publish:
	@if [ -e "$$HOME/.pypirc" ]; then \
		echo "Uploading to '$(CUSTOM_PIP_INDEX)'"; \
		python setup.py register -r "$(CUSTOM_PIP_INDEX)"; \
		python setup.py sdist upload -r "$(CUSTOM_PIP_INDEX)"; \
	else \
		echo "You should create a file called \`.pypirc' under your home dir.\n"; \
		echo "That's the right place to configure \`pypi' repos.\n"; \
		exit 1; \
	fi
