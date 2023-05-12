POETRY = $(HOME)/.local/bin/poetry
PYV = 3.11

dev: setup
	$(POETRY) install --with test,docs,dev
	$(POETRY) run pre-commit clean
	$(POETRY) run pre-commit install

devC: dev
	bash bin/deploy/post.sh

tests: setup
	$(POETRY) install --without docs,dev

build: setup
	$(POETRY) install --without test,docs,dev

docs: setup
	$(POETRY) install --with docs --without test,dev

setup:
	curl -sSL https://install.python-poetry.org | python3 -
	$(POETRY) env remove --all
	$(POETRY) config virtualenvs.in-project true
	pyenv install $(PYV) -s
	pyenv local $(PYV)
	$(POETRY) env use `pyenv which python`

uninstall:
	curl -sSL https://install.python-poetry.org | python3 - --uninstall

runAct:
	$(POETRY) shell

runCheck:
	$(POETRY) run pre-commit run --all-files

runDocs:
	$(POETRY) run mkdocs build -f configs/dev/mkdocs.yml -d ../../public

runTests:
	$(POETRY) run tox

runBuild:
	$(POETRY) build

runUpdate:
	$(POETRY) run pre-commit autoupdate \
	--repo https://github.com/python-poetry/poetry \
	--repo https://github.com/pre-commit/pre-commit-hooks \
	--repo https://github.com/psf/black \
	--repo https://github.com/charliermarsh/ruff-pre-commit \
	--repo https://github.com/pre-commit/mirrors-mypy \
	--repo https://github.com/jendrikseipp/vulture \
	--repo https://github.com/macisamuele/language-formatters-pre-commit-hooks \
	--repo https://github.com/codespell-project/codespell \
	--repo https://github.com/shellcheck-py/shellcheck-py
