#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#	that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=pulled_search test/unit/pulled_search/checks_dirs.py
coverage run -a --source=pulled_search test/unit/pulled_search/cleanup_files.py
coverage run -a --source=pulled_search test/unit/pulled_search/config_override.py
coverage run -a --source=pulled_search test/unit/pulled_search/create_json.py
coverage run -a --source=pulled_search test/unit/pulled_search/get_archive_files.py
coverage run -a --source=pulled_search test/unit/pulled_search/help_message.py
coverage run -a --source=pulled_search test/unit/pulled_search/insert_data.py
coverage run -a --source=pulled_search test/unit/pulled_search/load_processed.py
coverage run -a --source=pulled_search test/unit/pulled_search/main.py
coverage run -a --source=pulled_search test/unit/pulled_search/mvalidate_dirs.py
coverage run -a --source=pulled_search test/unit/pulled_search/non_processed.py
coverage run -a --source=pulled_search test/unit/pulled_search/process_docid.py
coverage run -a --source=pulled_search test/unit/pulled_search/process_failed.py
coverage run -a --source=pulled_search test/unit/pulled_search/process_files.py
coverage run -a --source=pulled_search test/unit/pulled_search/process_insert.py
coverage run -a --source=pulled_search test/unit/pulled_search/process_json.py
coverage run -a --source=pulled_search test/unit/pulled_search/recall_search.py
coverage run -a --source=pulled_search test/unit/pulled_search/run_program.py
coverage run -a --source=pulled_search test/unit/pulled_search/update_processed.py
coverage run -a --source=pulled_search test/unit/pulled_search/validate_dirs.py
coverage run -a --source=pulled_search test/unit/pulled_search/zgrep_search.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i

