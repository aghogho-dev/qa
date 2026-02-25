#!/bin/bash

echo "Starting Task 2 API Automated Tests..."

# Run all test in task_2 folder
pytest --html=task2_report.html --self-contained-html -s tests/task_2/


echo "Tests completed. Report generated: task2_report.html"