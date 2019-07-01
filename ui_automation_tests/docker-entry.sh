#!/usr/bin/env bash

# DEBUG
set -x
set -e
echo $PWD
touch $PWD/test_ran.txt

# run py.test ($@ to derive parameters from commandline)
py.test --alluredir=allure-results $@ &
pid="$!"

# trap process id to stop script using Control+C
trap "echo '=== Stopping PID $pid ==='; kill -SIGTERM $pid" SIGINT SIGTERM

wait $pid
