#!/usr/bin/env bash

set -x

parallel_option=''
# run py.test ($@ to derive parameters from commandline)
if [ $NO_OF_PARALLEL_RUNNERS -gt 1 ]
then
    py.test -k "$TESTS_TO_RUN" "$parallel_option" --dist=loadscope --ignore=core --alluredir=ui_automation_tests/allure-results &
else
    py.test -k "$TESTS_TO_RUN" --dist=loadscope --ignore=core --alluredir=ui_automation_tests/allure-results &
fi
pid="$!"

# trap process id to stop script using Control+C
trap "echo '=== Stopping PID $pid ==='; kill -SIGTERM $pid" SIGINT SIGTERM

wait $pid
