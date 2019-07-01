#!/usr/bin/env bash

# DEBUG
set -x
set -e
mount
ls -al /var/lib/jenkins/lite/workspace/exporter_frontend_e2e_tests
echo $PWD
ls -al $PWD
touch $PWD/test_ran.txt

# run py.test ($@ to derive parameters from commandline)
py.test --alluredir=allure-results $@ &
pid="$!"

# trap process id to stop script using Control+C
trap "echo '=== Stopping PID $pid ==='; kill -SIGTERM $pid" SIGINT SIGTERM

wait $pid
