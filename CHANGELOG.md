# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.

## [0.1.0] - 2020-03-13
### Fixed
- process_docid:  Seralize the json document before inserting into RabbitMQ.

### Added
- process_insert:  Process the insert file and send to a database.
- config_override:  Checks for specific arguments which will override the values for some configuration settings.
- mvalidate_dirs:  Validate the directories in the configuration file for the -I option.
- checks_dirs:  Validate the directories in the configuration file depending on the options selected.
- setup_mail: Create mail instance.
- cleanup_files:  Send processed files to destination directory and remove from master file list.
- process_list:  Processes the docid files.
- insert_data:  Insert pulled search files into Mongodb.
- Added -n and -I options to program which designates directory to monitor for Pulled Search files.

### Changed
- run_program:  Replaced validate_dirs with checks_dirs call.
- run_program:  Replaced checking config settings with call to config_override.
- config/search.py.TEMPLATE:  Added section for Mongodb configuration.
- non_processed:  Added check to see if there were non-processed files.
- process_files:  Replaced sections of code with calls to general functions.
- main:  Added -n option.
- main:  Added function calls dictionary for different options.
- main:  Added -n and -I options along with additional Xor check.
- run_program:  Added code to use the function dictionary.


## [0.0.2] - 2020-03-09
### Added
- dir_file_search:  Return a list of files in a directory matching a string.
- date_range:  Return a list of year-month combinations between two dates.
- get_archive_files:  Added function to search of list of archive log files.
- month_days:  Return the number of days in the month in the date.

### Changed
- process_files:  Archive docid files instead of removing them.
- validate_dirs:  Added archive directory check.
- process_docid:  Added exception handling for removing files.
- process_files:  Changed gen_libs.dir_file_match to dir_file_search.
- process_docid:  Changed gen_libs.dir_file_match to dir_file_search.
- process_docid:  Converted command name to lowercase for log file search.
- process_docid:  Special case exception for one command.
- process_docid:  Setup cmd variable separately for later use in archive searches.
- process_docid:  Added args_array to args parameter list.
- process_docid:  Added call to get archive log files to search.
- process_files:  Added args_array to process_docid call.

### Fixed
- process_docid:  Changed cmd_regex to a regular expression.
- run_program:  Replaced gen_libs.chk_crt_file call with gen_libs.chk_crt_dir call.
- validate_dirs:  Replaced gen_libs.chk_crt_file calls with gen_libs.chk_crt_dir calls.
- Changed cfg.docid_dir to cfg.doc_dir to fix incorrect reference.
- Replaced postdate with pubdate to be in align with the Doc ID file.
- config/search.py.TEMPLATE:  Changed logfile to log_file.


## [0.0.1] - 2020-03-03
- Initial creation.

