# Python project for searching for entries for a pulled product in log files.
# Classification (U)

# Description:
  The pulled_search program will detect when new pulled product files are created, parse the file, call the check_log program to check log files for the docid in the file, any entries found will be converted into a JSON document and send to a RabbitMQ queue.

###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Help Function
  * Testing
    - Unit


# Features:
  * Locate docids in log files and sends them to RabbitMQ.


# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/arg_parser
    - lib/gen_class
    - lib/gen_libs
    - rabbit_lib/rabbit_class
    - mongo_lib/mongo_libs
    - mongo_lib/mongo_class
    - checklog/check_log


# Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/pulled-search.git
```

Install/upgrade system modules.

```
cd pulled-search
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-check-log.txt --target checklog --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target checklog/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Initialize configuration file.
```
cd config
cp search.py.TEMPLATE search.py
```

Make the appropriate changes to the environment.
  * Make the appropriate changes to connect to General setup section.
    - doc_dir = "DOC_DIR_PATH"
    - file_regex = "_docid.json"
    - log_dir = "LOG_DIR_PATH"
    - log_type = "access_log"
    - outfile = "DIR_PATH/checklog.out"
    - enclave = "ENCLAVE"
    - error_dir = "ERROR_DIR_PATH"
    - archive_dir = "ARCHIVE_DIR_PATH"
    - log_file = "DIR_PATH/pulled_search.log"
    - admin_email = "USERNAME@EMAIL_DOMAIN"

  * Make the appropriate changes to connect to RabbitMQ section.
    - user = "USER"
    - pswd = "PSWD"
    - host = "HOSTNAME"
    - queue = "QUEUENAME"
    - r_key = "RKEYNAME" (Normally the same as the queue name.)
    - exchange_name = "EXCHANGE_NAME"

```
vim search.py
chmod 600 search.py
```

# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/pulled-search/pulled_search.py -h
```


# Testing:

# Unit Testing:

### Description: Testing consists of unit testing for the functions in the pulled_search.py program.

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/pulled-search.git
```

Install/upgrade system modules.

```
cd pulled-search
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-check-log.txt --target checklog --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target checklog/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Unit test runs for pulled_search.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/pulled-search
test/unit/pulled_search/cleanup_files.py
test/unit/pulled_search/create_json.py
test/unit/pulled_search/create_rmq.py
test/unit/pulled_search/date_range.py
test/unit/pulled_search/dir_file_search.py
test/unit/pulled_search/get_archive_files.py
test/unit/pulled_search/help_message.py
test/unit/pulled_search/insert_data.py
test/unit/pulled_search/main.py
test/unit/pulled_search/month_days.py
test/unit/pulled_search/non_processed.py
test/unit/pulled_search/process_docid.py
test/unit/pulled_search/process_files.py
test/unit/pulled_search/process_list.py
test/unit/pulled_search/run_program.py
test/unit/pulled_search/send_2_rabbitmq.py
test/unit/pulled_search/setup_mail.py
test/unit/pulled_search/validate_dirs.py
```

### All unit testing
```
test/unit/pulled_search/unit_test_run.sh
```

### Code coverage program
```
test/unit/pulled_search/code_coverage.sh
```

