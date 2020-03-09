#!/bin/bash
# Unit testing program for the pulled_search.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  pulled_search.py"
test/unit/pulled_search/create_json.py
test/unit/pulled_search/create_rmq.py
test/unit/check_log/help_message.py
test/unit/pulled_search/main.py
test/unit/pulled_search/non_processed.py
test/unit/pulled_search/process_docid.py
test/unit/pulled_search/process_files.py
test/unit/pulled_search/run_program.py
test/unit/pulled_search/send_2_rabbitmq.py
test/unit/pulled_search/validate_dirs.py
