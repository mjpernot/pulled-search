# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.

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
- create_json:  Changed JSON document to CamelCase.
- get_archive_files:  Replaced date_range call with gen_libs.date_range call.
- insert_data:  Replaced dir_file_search call with gen_libs.filename_search call.
- process_files:  Replaced dir_file_search call with gen_libs.filename_search call.
- process_docid:  Replaced dir_file_search call with gen_libs.filename_search call.
- get_archive_files:  Replaced dir_file_search call with gen_libs.filename_search call.
- insert_data:  Replaced setup_mail call with gen_class.setup_mail call and added -s option to subject line.
- process_files:  Replaced setup_mail call with gen_class.setup_mail call and added -s option to subject line.
- config/search.py.TEMPLATE:  Removed admin_email entry.
- run_program:  Removed admin emails and replaced with print commands or log entries.
- Documentation updates.

### Removed
- dir_file_search function.
- date_range function.
- month_days function.
- send_2_rabbitmq function.
- create_rmq function.
- setup_mail function.


## [0.1.1] - 2020-03-20

### Added
- zgrep_search:  Zgrep compressed files for keyword and write to file.

### Changed
- send_2_rabbitmq:  Added drop_connection call after publishing data to RabbitMQ.
- create_rmq:  Changed several parameters to keyword arguments in rabbitmq_class.RabbitMQPub call.
- process_docid:  Check for pre-Centos 7 OS to call zgrep_search instead of calling check_log.


## [0.1.0] - 2020-03-13
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

