# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [0.2.14] - 2025-03-18
Breaking Changes

- Removed support for Python 2.7.
- Add pre-header check on allowable Python versions to run.
- Updated urllib3==1.26.20
- Added certifi==2024.12.14
- Updated pymongo==4.10.1
- Updated rabbitmq-lib to v2.3.0
- Updated mongo-lib to v4.5.1
- Updated python-lib to v4.0.0
- Updated check-log to v5.0.0

### Added
- process_data: Convert data from file into dictionary list.
- rm_file: Remove file.

### Changed
- Refactored open file command and added "encoding" argument to open() command.
- Replaced dict() with {} and list() with [].
- Converted strings to f-strings.
- Documentation changes.

### Removed
- Mongo 3.4 support.


## [0.2.13] - 2024-11-25
Breaking Change.
- This version going forward will work only for Python 3.

- Updated distro==1.9.0 for Python 3.
- Added idna==2.10 for Python 3.
- Updated pika==1.3.1 for Python 3.
- Updated psutil==5.9.4 for Python 3.
- Updated requests==2.25.0 for Python 3.
- Updated urllib3==1.26.19 for Python 3.
- Updated simplejson==3.13.2 for Python 3.
- Updated six==1.16.0 for Python 3.
- Updated python-lib to v3.0.8
- Updated rabbitmq-lib to v2.2.7
- Updated mongo-lib to v4.3.4
- Updated check-log to v4.2.3

### Fixed
- is_base64: Added exception to handle incorrect buffering error for Python 3.

### Changed
- process_insert: Added decode to base64 command in ast.literal_eval check to convert bytes back to string for comparsion.
- is_base64: Added decode to base64 command to convert bytes back to string for comparsion.

### Deprecated
- Support for Python 2.7


## [0.2.12] - 2024-09-27
- Updated pymongo==4.1.1 for Python 3.6
- Updated simplejson==3.13.2 for Python 3
- Updated mongo-lib to v4.3.2
- Updated python-lib to v3.0.5
- Updated check-log to v4.2.1
- Updated rabbitmq-lib to v2.2.6


## [0.2.11] - 2024-08-07
- Updated simplejson==3.13.2
- Updated requests==2.25.0
- Added certifi==2019.11.28
- Added idna==2.10
- Removed email==4.0.3

### Changed
- Updates to requirements.txt.


## [0.2.10] - 2024-07-30
- Set urllib3 to 1.26.19 for Python 2 for security reasons.
- Updated rabbitmq-lib to v2.2.4


## [0.2.9] - 2024-06-20
- Parse the data before it is email, inserted into Mongo or published to RabbitMQ.

### Added
- filter_data: Filter out non-required data entries.

### Changed
- mvalidate_dirs: Refactored to only contains those options that use the Mongo insert option.
- validate_dirs: Refactored to only contain those checks common to both -F and -P options.
- checks_dirs: Added -F option check and unique checks for -P and and -I options.
- insert_mongo: Removed any reference to unparsed.
- main: Removed parsing from gen_class.ArgParser call and called arg_parse2 as part of "if" statement, removed the XOR check for the output options (-i, -e, -r) to allow for multiple outputs.
- parse_data: Removed the filtering of data from the process, done in filter_data function.
- process_json: Added call to filter_data to remove non-required entries, add check to email to send data via email body or attachement.
- config/search.py.TEMPLATE: Added raw_archive_dir and unparsable_dir entries.
- config/mongo.py.TEMPLATE:  Removed unparsed entry.
- Documentation updates.


## [0.2.8] - 2024-05-28
- Add ability to send Mongo inserts via email body instead of as an attachment.

### Changed
- process_json: Check to see if to send data as attachment or in the body of the email.
- Documentation updates.


## [0.2.7] - 2024-05-15
- Added filters to remove non-related entries.

### Changed
- insert_mongo: Added check for unparsed entries, write insert error data out to a file and added email capability.
- parse_data: Added checks to remove non-related entries from being inserted into Mongo database and insert unparsed data into another collection.
- config/mongo.py.TEMPLATE: Added collection name for unparsed entries: unparsed


## [0.2.6] - 2024-04-23
- Updated mongo-lib to v4.3.0
- Added TLS capability for Mongo
- Set pymongo to 3.12.3 for Python 2 and Python 3.

### Changed
- Set pymongo to 3.12.3 for Python 2 and Python 3.
- config/mongo.py.TEMPLATE: Added TLS entries.
- Documentation updates.


## [0.2.5] - 2024-03-07
- Updated to work in Red Hat 8
- Updated rabbitmq-lib to v2.2.3
- Updated mongo-lib to v4.2.9
- Updated python-lib to v3.0.3
- Updated check-log to v4.0.7

### Fixed
- process_files: Checks to see if search directory exists.
- parse: Added delimiter (.) in the archive file name.
- config/search.py.TEMPLATE: Fixed eucom entry.

### Changed
- config/search.py.TEMPLATE: Added acic to command.
- process_json: Removed gen_libs.get_inst call.
- Set simplejson to 3.12.0 for Python 3.
- Set chardet to 3.0.4 for Python 2.
- Documentation updates.


## [0.2.4] - 2023-06-27
### Fixed
- parse_data: Corrected incorrect keyword argument to gen_libs.write_file.

### Changed
- main: Removed gen_libs.get_inst call.


## [0.2.3] - 2023-06-08
- Updated check-log to v4.0.4
- Merged archive_log_dir config entry into log_dir.
- Added archive of logs for the -i option.

### Fixed
- checklog/check_log: Fixed sending out empty emails.

### Changed
- is_base64, process_insert: Removed unused err variable.
- parse_data: Added write data to an archive directory.
- validate_dirs: Removed -a check and removed cfg.archive_log_dir directory check.
- process_docid: Replaced cfg.archive_log_dir with cfg.log_dir.
- config/search.py.TEMPLATE: Removed archive_log_dir entry.
- Documentation updates.


## [0.2.2] - 2023-05-22
- Add ability to create summary report when emailing out docid findings.

### Added
- write_summary: Write summary results for docid to docid transfer file.

### Changed
- process_json: Call to write_summary if email and -b option are selected.


## [0.2.1] - 2023-05-15
### Fixed
- process_insert: Will not stacktrace if file is a string.

### Added
- is_base64: Determines if the data is base64 encoded.

### Changed
- config/search.py.TEMPLATE:  Added "CN=" to the userid tag in the regex entry.
- Documentation updates.


## [0.2.0] - 2023-05-11
Beta release

### Fixed
- process_insert: Added eval call to the log_json variable assignment.
- process_json: Added set_payload call to add attachment.


## [0.1.9] - 2023-04-25
- Added pulldate for docids coming in via file.
- Added -e and -r options for the -P and -F options.
- Upgraded python-lib to v2.10.1

### Fixed
- process_json: Replace the gen_class.Mail with email and smptlib code to send data as an attachment.
- main: Added -F option to opt_val_list variable.

### Changed
- process_insert: Added code to read a file, decode it and convert it to JSON.
- get_archive_files: Set end datetime to pulldate if exists otherwise use current datetime.
- process_docid: Determine if pulldate exist for -a (archive) option and pass to get_archive_files call.
- cleanup_files: Added destination directory to the log entry when archiving the file.
- recall_search2: Passed pulldate to the search_docid call.
- file_input: Parsed pulldate from input file.
- main: Changed gen_libs.help_func call to pass ArgParser class instance.
- process_json: Added email subject to log entry when using mail option.
- Documentation updates.


## [0.1.8] - 2023-03-28
- Added ability to search for docids via an input file.

### Changed
- main: Added gen_class.ArgsParser.arg_file_chk call to check -F option file.
- load_processed, recall_search, update_processed: Changed from filenames to docids.
- recall_search: Replaced sections of code with calls to search_docidi and remove_processed.
- process_files: Removed YYYYMM from end of processed file name, all processed files will be stored in one file.
- process_files, validate_dirs: Replaced cfg.processed_dir with cfg.processed_file.
- config/search.py.TEMPLATE: Combined processed_dir and processed_file entries into processed_file.
- Documentation update.

### Added
- recall_search2: Get docids from an input file and process the docids.
- file_input: Process docids via input file.
- remove_processed: Removes any previous processed docids from the file_dict.
- search_docid: Call the process_docid and check on status of docid.


## [0.1.7] - 2023-03-09
### Fixed
- process_docid: Added check in to see if check_log outfile exists.
- parse_data: Moved insert into mongo to the correct location and return the correct status code.

### Changed
- process_insert: Replaced insert into Mongo code with call to parse_data.
- config/search.py.TEMPLATE: Updated the regular expression to break verb into verb and verbUrl.

## [0.1.6] - 2023-02-27
### Fixed
- validate_dirs: Active log directory config entry is not checked if searching archive logs.
- process_docid: If check_log does not produce an out file.
- recall_search: Fixed pulling the date time group and docid from the filename.

### Changed
- process_docid: Set the out file for check_log to be a unique file name.
- parse_data: Refactored the regular expression to match Highpoint access logs format and moved into the config file.  Also added ability to determine which tags to add to the final document from the parsed log entry.


## [0.1.5] - 2023-02-03
- Allow searches to insert into the Mongo database directly.
- Each log entry detected will be its own document within the Mongo database, but will still be grouped into a list for emails and RabbitMQ usage.
- Parse the log entry into subsections if possible.
- Removed support for Centos 6 servers and below.

### Fixed
- recall_search: Pubdate being captured incorrectly from filename string.

### Added
- parse_data: Parse data prior to inserting in Mongo database.
- insert_mongo: Insert data document into Mongo.

### Changed
- process_docid: Removed the check for Centos 6 usage and calling zgrep_search.

### Removed
- Removed -z option.
- zgrep_search
- create_json


## [0.1.4] - 2022-10-13
- Refactoring the input of the Docid files, will grab the Docid data from the Pulled html files directly.
- Updated to work in Python 3 too
- Upgraded python-lib to v2.9.4
- Upgraded mongo-lib to v4.2.2
- Upgraded rabbitmq-lib to v2.2.1
- Upgraded check-log to v4.0.2

### Fixed
- process_docid: Status was not being set correctly.

### Added
- load_processed: Read in the previous processed file names.
- update_processed: Update the processed file with new file entries.
- process_failed: Process the failed files.
- recall_search: Search for security recalled products in the pulled files and process those files.

### Changed
- process_json: Added status return on the publishing of data to RabbitMQ.
- insert_data: Added code to create the remove file list.
- process_files: Refactored the function and broke out code into individual functions.
- validate_dirs: Added new directory check.
- config_override: Removed check on the -m option.
- process_docid: Removed code for setting up docid_dict, handled outside of function now. 
- run_program: Added YYYYMMDD to the Logger file name for log file rotation.
- Documentation updates.

### Removed
- process_list


## [0.1.3] - 2021-12-15
- Upgraded check-log to v4.0.1
- Upgrade mongo-libs to v4.2.1
- Upgrade python-lib to v2.9.3

### Added
- process_json: Process the JSON document from the pulled search results by either emailing them or publishing them to RabbitMQ.

### Changed
- process_docid: Create gen_class.ArgParser class instance for the check_log.run_program call, replaced hardcoding of command check with configuration check and added call to process_json.
- Multiple functions: Replaced the use of arg_parser (args_array) with gen_class.ArgParser class (args).
- process_insert:  Captured and processed status return from mongo_libs.ins_doc call.
- config/mongo.py.TEMPLATE:  Added SSL connection entriesi and removed some old entries.
- config/search.py.TEMPLATE:  Added entry to connect to RabbitMQ cluster and email option entriesi and added command-keyword entry.
- Documentation updates.

### Removed
- Removed support for Python 2.6


## [0.1.2] - 2020-07-01
### Fixed
- main: Fixed handling command line arguments from SonarQube scan finding.
- zgrep_search:  Fixed handling subprocess line from SonarQube scan finding.
- process_list:  Fixed log entries.

### Changed
- process_docid:  Refactored the check on the command being processed.
- process_docid:  Implemented the -z option to use the zgrep search capability.
- process_docid:  Added check on return status from rabbitmq_class.pub_2_rmq.
- process_docid:  Replaced send_2_rabbitmq call with rabbitmq_class.pub_2_rmq call.
- create_json:  Changed JSON document to PascalCase.
- get_archive_files, insert_data, process_files, process_docid: Replaced date_range call with gen_libs.date_range call.
- insert_data, process_files:  Replaced setup_mail call with gen_class.setup_mail call and added -s option to subject line.
- config/search.py.TEMPLATE:  Removed admin_email entry.
- run_program:  Removed admin emails and replaced with print commands or log entries.
- Documentation updates.

### Removed
- dir_file_search
- date_range
- month_days
- send_2_rabbitmq
- create_rmq
- setup_mail


## [0.1.1] - 2020-03-20

### Added
- zgrep_search:  Zgrep compressed files for keyword and write to file.

### Changed
- send_2_rabbitmq:  Added drop_connection call after publishing data to RabbitMQ.
- create_rmq:  Changed several parameters to keyword arguments in rabbitmq_class.RabbitMQPub call.
- process_docid:  Check for pre-Centos 7 OS to call zgrep_search instead of calling check_log.


## [0.1.0] - 2020-03-13
- Alpha version release.

### Fixed
- process_docid:  Seralize the json document before inserting into RabbitMQ.

### Added
- config/mongo.py.TEMPLATE:  Seperate configuration file for the Mongodb instance setup.
- process_insert:  Process the insert file and send to a database.
- config_override:  Checks for specific arguments which will override the values for some configuration settings.
- mvalidate_dirs:  Validate the directories in the configuration file for the Insert option.
- checks_dirs:  Validate the directories in the configuration file depending on the options selected.
- setup_mail: Create mail instance.
- cleanup_files:  Send processed files to destination directory and remove from master file list.
- process_list:  Processes the docid files.
- insert_data:  Insert pulled search files into Mongodb.
- Added Insert option to program monitors for files to be insert into a Mongo database.

### Changed
- run_program:  Replaced validate_dirs with checks_dirs call, replaced checking config settings with call to config_override, and added code to use the function dictionary.
- config/search.py.TEMPLATE:  Added section for Insert configuration.
- non_processed:  Added check to see if there were non-processed files.
- process_files:  Replaced sections of code with calls to general functions.
- main:  Added function calls dictionary for different options and added -n and -I options along with additional Xor check.


## [0.0.2] - 2020-03-09
### Added
- dir_file_search:  Return a list of files in a directory matching a string.
- date_range:  Return a list of year-month combinations between two dates.
- get_archive_files:  Added function to search of list of archive log files.
- month_days:  Return the number of days in the month in the date.

### Changed
- process_files:  Archive docid files instead of removing them.
- validate_dirs:  Added archive directory check.
- process_files:  Changed gen_libs.dir_file_match to dir_file_search and added args_array to process_docid call.
- process_docid:  Added exception handling for removing files, changed gen_libs.dir_file_match to dir_file_search, converted command name to lowercase for log file search, special case exception for one command, setup cmd variable separately for later use in archive searches, added args_array to args parameter list, and added call to get archive log files to search.

### Fixed
- process_docid:  Changed cmd_regex to a regular expression.
- run_program:  Replaced gen_libs.chk_crt_file call with gen_libs.chk_crt_dir call.
- validate_dirs:  Replaced gen_libs.chk_crt_file calls with gen_libs.chk_crt_dir calls.
- Changed cfg.docid_dir to cfg.doc_dir to fix incorrect reference.
- Replaced postdate with pubdate to be in align with the Doc ID file.
- config/search.py.TEMPLATE:  Changed logfile to log_file.


## [0.0.1] - 2020-03-03
- Initial creation.

