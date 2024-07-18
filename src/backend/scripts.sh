#!/bin/bash
set -ex

PROJECT_PATH=.

tests () {
  pytest $PROJECT_PATH
}

check_flake () {
  flake8 $PROJECT_PATH
}

check_imports () {
  autoflake -r --remove-all-unused-imports --ignore-init-module-imports --exclude .venv . && isort --skip .venv . -c
}

check_black () {
  black $PROJECT_PATH --check
}

check_codestyle () {
  check_flake
  check_imports
  check_black
}

optimize_imports () {
  isort $PROJECT_PATH --float-to-top --skip .venv && \
  autoflake -i -r --remove-all-unused-imports --ignore-init-module-imports --exclude node_modules . && \
  isort $PROJECT_PATH --float-to-top --skip .venv
}

format_black () {
  black $PROJECT_PATH
}

format () {
  optimize_imports
  format_black
}

check () {
  check_codestyle
  tests
}

$1
