# Python project for searching for entries for a pulled product in log files and inserting them into a database.
# Classification (U)

# Description:
  The pulled_search program is a multi-optional program for use with the pulled product process.  It can detect when new pulled product files are created, parse the file, call the search program to check log files for the docid in the file.  Any entries found will be converted into a JSON document and send to a RabbitMQ queue.  The program also has the ability to detect when new search pulled product log entries are available to be inserted into a database.

###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
    - Secure Environment
  * Installation
  * Configuration
  * Program Help Function
  * Testing
    - Unit


# Features:
  * Monitor directory for DocID files that will be used to search log files with corresponding log entries.
  * Parse and convert log entries into a JSON document and send them to a RabbitMQ queue.
  * Monitor directory for Pulled Product searched json log entries.
  * Parse and convert pulled product json log entries and insert them into a Mongodb database.

### Notes:
  *  The monitor and insert into Mongo database option (-I option) is normally used in conjunction with the rmq-sysmon program.  The rmq-sysmon program is used to monitor RabbitMQ queues and write messages in the queue out to a file.


# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - python3-pip
    - python3-devel
    - gcc

  * Secure Environment:  If operating in a secure environment, this package will require at least a minimum of pymongo==3.8.0 or better.  It will also require a manual change to the auth.py module in the pymongo package.  See below for changes to auth.py.  In addition, other modules may require to have the same modification as the auth.py module.  If a stacktrace occurs and it states "= hashlib.md5()" is the problem, then note the module name "= hashlib.md5()" is in and make the same change as in auth.py:  "usedforsecurity=False".
    - Locate the auth.py file python installed packages on the system in the pymongo package directory.
    - Edit the file and locate the \_password_digest function.
    - In the \_password_digest function there is an line that should match: "md5hash = hashlib.md5()".  Change it to "md5hash = hashlib.md5(usedforsecurity=False)".
    - Lastly, it will require the configuration file entry auth_mech to be set to: SCRAM-SHA-1 or SCRAM-SHA-256.


# Installation:

Install the project using git.

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/pulled-search.git
```

Install/upgrade system modules.

NOTE: Install as the user that will run the program.

Redhat 8 (Running Python 3.9 and 3.12):

```
python -m pip install --user -r requirements39.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```

Install supporting classes and libraries.

```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-check-log.txt --target checklog --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-checklog-python-lib.txt --target checklog/lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-checklog-python-lib.txt --target checklog/lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mongo-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

### Initialize configuration file.

Make the appropriate changes to the environment.
  * Make the appropriate changes to General setup section.
  * This section is for either the -P or -I option.
    - log_file = "DIR_PATH/pulled_search.log"

  * Make the appropriate changes to Process/Search setup section.
  * This section is for all options -F and -P options.
    - raw_archive_dir = "BASE_PATH/raw_archive"
    - unparsable_dir = "BASE_PATH/unparsable"

  * Update this section if using the -P option.
    - doc_dir = ["DOC_DIR_PATH", "DOC_DIR_PATH2"]
    - processed_file = "BASE_PATH/processed/processed"
    - outfile = "BASE_PATH/tmp/checklog.out"
    - error_dir = "BASE_PATH/search_error"
    - enclave = "ENCLAVE"
    - log_dir = "LOG_DIR_PATH"

  * These options will not need to be updated normally.
    - file_regex = "-PULLED-"
    - pattern = "JAC.pull.subtype.\*.SECURITY RECALL"
    - log_type = "access_log"
    - command = {"eucom": "intelink", "acic": "usacic"}

  * Make the appropriate changes to RabbitMQ section.
  * Update this section if using the -P option.
    - to_addr = None
    - subj = None
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOSTNAME"
    - host_list = []
    - queue = "QUEUENAME"
    - r_key = "ROUTING_KEY"
    - exchange_name = "EXCHANGE_NAME"
  * Do not change this section unless you have knowledge with RabbitMQ.
    - port = 5672
    - exchange_type = "direct"
    - x_durable = True
    - q_durable = True
    - auto_delete = False

  * Make the appropriate changes to Insert setup section.
  * Update this section if using the -I option.
    - monitor_dir = "MONITOR_DIR_PATH"
    - mfile_regex = "\_mongo.json"

  * These entries are for the -i and -I options (mongo database).
    - marchive_dir = "BASE_PATH/archive
    - merror_dir = "BASE_PATH/mongo_error"
  * Do not change this section unless the Mongo configuration file is changed.
    - mconfig = "mongo"

  * Log parsing section.
  * Warning: Do not modify this section unless you know regular expressions.
    - regex = "(?P\<ip\>.\*?) (?P\<proxyid\>.\*?) (?P\<userid\>.\*?) \[(?P\<logTime\>.\*?)(?= ) (?P\<timeZone\>.\*?)\] (?P\<requestid\>.\*?) (?P\<secs\>.\*?)/(?P\<msecs\>.\*?) \"(?P\<verb\>.\*?) HTTP/(?P\<httpVer\>.\*?)\" (?P\<status\>.\*?) (?P\<length\>.\*?) \"(?P\<referrer\>.\*?)\" \"(?P\<userAgent\>.\*?)\" (?P\<url\>.\*?)?$"
    - allowable = ["userid", "logTime", "verb", "status", "url"]

```
cp config/search.py.TEMPLATE config/search.py
vim config/search.py
chmod 600 config/search.py
```

Create Mongodb configuration file.  Make the appropriate change to the environment.
  * Make the appropriate changes to connect to a Mongo database.
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"

  * Change these entries only if required:
    - port = 27017
    - conf_file = None
    - auth = True
    - auth_db = "admin"
    - auth_mech = "SCRAM-SHA-1"

  * Notes for auth_mech configuration entry:
    - NOTE 1:  SCRAM-SHA-256 only works for Mongodb 4.0 and better.
    - NOTE 2:  Secure environment requires SCRAM-SHA-1 or SCRAM-SHA-256.

  * If connecting to a Mongo replica set, otherwise set to None.
    - repset = "REPLICA_SET_NAME"
    - repset_hosts = "HOST_1:PORT, HOST_2:PORT, ..."
    - db_auth = "AUTHENTICATION_DATABASE"

  * If Mongo is set to use TLS or SSL connections, then one or more of the following entries will need to be completed to connect using TLS or SSL protocols.  Note:  Read the configuration file to determine which entries will need to be
set.
    - SSL:
        -> auth_type = None
        -> ssl_client_ca = None
        -> ssl_client_key = None
        -> ssl_client_cert = None
        -> ssl_client_phrase = None
    - TLS:
        -> auth_type = None
        -> tls_ca_certs = None
        -> tls_certkey = None
        -> tls_certkey_phrase = None 

  * Secure Environment for Mongo:  See Prerequisites -> Secure Environment section for details.

  * Set the database and collection names where the data will be inserted into.
    - dbs = "DATABASE"
    - tbl = "COLLECTION"

```
cp config/mongo.py.TEMPLATE config/mongo.py
vim config/mongo.py
chmod 600 config/mongo.py
```


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
pulled_search.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
test/unit/pulled_search/unit_test_run.sh
test/unit/pulled_search/code_coverage.sh
```

