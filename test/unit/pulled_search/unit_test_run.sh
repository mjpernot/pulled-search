#!/bin/bash
# Unit testing program for the pulled_search.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  pulled_search.py"
/usr/bin/python ./test/unit/pulled_search/checks_dirs.py
/usr/bin/python ./test/unit/pulled_search/cleanup_files.py
/usr/bin/python ./test/unit/pulled_search/config_override.py
/usr/bin/python ./test/unit/pulled_search/get_archive_files.py
/usr/bin/python ./test/unit/pulled_search/help_message.py
/usr/bin/python ./test/unit/pulled_search/insert_data.py
/usr/bin/python ./test/unit/pulled_search/insert_mongo.py
/usr/bin/python ./test/unit/pulled_search/load_processed.py
/usr/bin/python ./test/unit/pulled_search/main.py
/usr/bin/python ./test/unit/pulled_search/mvalidate_dirs.py
/usr/bin/python ./test/unit/pulled_search/non_processed.py
/usr/bin/python ./test/unit/pulled_search/parse_data.py
/usr/bin/python ./test/unit/pulled_search/process_docid.py
/usr/bin/python ./test/unit/pulled_search/process_failed.py
/usr/bin/python ./test/unit/pulled_search/process_files.py
/usr/bin/python ./test/unit/pulled_search/process_insert.py
/usr/bin/python ./test/unit/pulled_search/process_json.py
/usr/bin/python ./test/unit/pulled_search/recall_search.py
/usr/bin/python ./test/unit/pulled_search/remove_processed.py
/usr/bin/python ./test/unit/pulled_search/run_program.py
/usr/bin/python ./test/unit/pulled_search/search_docid.py
/usr/bin/python ./test/unit/pulled_search/update_processed.py
/usr/bin/python ./test/unit/pulled_search/validate_dirs.py
