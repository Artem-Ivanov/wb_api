# wb_api

#### Make sure you have `python3.12` installed in system:
```bash
python3 -v # 3.12+
```
or
```bash
which python3.12 # should show you path to interpreter
```
If not, you can install it using package manager or `pyenv` (Python Version Management), see documentation [here](https://github.com/pyenv/pyenv)

#### Install the Poetry (v1.6.1 is highly recommended):
```bash
curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 python3.12 -
```

If you have any issues check the [poetry documentation](https://python-poetry.org/docs/#installing-with-the-official-installer).

#### Setup backend project by installing dependencies:
```bash
cd src/backend
poetry install
```

#### Run the shell with the activated virtual environment:
```bash
poetry shell
```
More about deploying project locally see [docs](https://wiki.1cupis.org/pages/viewpage.action?pageId=138098503)

#### Install pre-commit hook:
Type this command in terminal to install pre-commit hook (only auto-formatting and linting)
```bash
pre-commit install --hook-type pre-commit
```
or if you would like also to run tests on **push** to server run this
```bash
pre-commit install --hook-type pre-commit --hook-type pre-push
```
You can disable **only** pre-push hook by command but leave pre-commit as it is
```bash
pre-commit uninstall --hook-type pre-push
```
or uninstall everything completely with
```bash
pre-commit uninstall --hook-type pre-commit --hook-type pre-push
```

#### Start project
```bash
python manage.py runserver
```
#### Start Kafka worker
```bash
python manage.py runworker
```

#### Start celery beat
```bash
celery -A settings beat -l INFO -S django
```

#### Run celery worker with beat together
```bash
celery -A settings worker --beat --scheduler django --loglevel=debug -Q MANUAL_ACTION,SCHEDULER_ACTION
```
