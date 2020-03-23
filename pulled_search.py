#!/usr/bin/python
# Classification (U)

"""Program:  pulled_search.py

    Description:  The pulled_search program monitors for new files that contain
        docids.  Once detected will search the Apache log files for any entries
        and if detected will send these log entries to a RabbitMQ queue.

    Usage:
        pulled_search.py -c file -d path [-m path | -n path | -z | -P | -I |
            -y flavor_id | -a] [-t email {email2 email3 ...} {-s subject_line}]
            [-v | -h]

    Arguments:
        -P => Process Doc ID files send to RabbitMQ.
        -I => Insert Pulled Search files into Mongodb.
        -c file => Configuration file.  Required argument.
        -d dir_path => Directory path for option '-c'.  Required argument.
        -m dir_path => Directory to monitor for doc ID files.
        -n dir_path => Directory to monitor for pulled search files.
        -a => This is an archive log search.
        -z => Use the zgrep option instead of check_log to check GZipped files.
        -t email_address(es) => Send output to one or more email addresses.
        -s subject_line => Subject line of email.  Requires -t option.
        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.
        NOTE 2:  -s requires -t option to be included.
        NOTE 3:  -P and -I are Xor options.
        NOTE 4:  -m and -n options will override the configuration settings.
            The -m option is mapped to the doc_dir configuration entry, and
            the -n option is mapped to the monitor_dir configuration entry.
        NOTE 5:  The log files can be normal flat files or compressed files
            (e.g. ending with .gz) or a combination there of.  Any other type
            of compressed file will not work.

    Configuration files:
        Configuration file (config/search.py.TEMPLATE).  Below is the
        configuration file format for the environment setup in the program.

            # Pulled Search General Configuration section.
            # Logger file for the storage of log entries.
            # File name including directory path.
            log_file = "DIR_PATH/pulled_search.log"
            # Administrator email for reporting errors detected during the
            #   program run.
            admin_email = "USERNAME@EMAIL_DOMAIN"

            # Pulled Search Process Configuration section.
            # Directory where docid files to be processed are.
            doc_dir = "DOC_DIR_PATH"
            # Regular expression for search for log file names.
            file_regex = "_docid.json"
            # Directory where log files to be searched are.
            log_dir = "LOG_DIR_PATH"
            # Type of log files to checked.
            log_type = "access_log"
            # Temporary file where check_log will write to.
            # File name including directory path.
            outfile = "DIR_PATH/checklog.out"
            # Security enclave these files are being processed on.
            enclave = "ENCLAVE"
            # Directory path to where error and non-processed files are saved
            #   to.
            archive_dir = "ARCHIVE_DIR_PATH"
            # Directory path to where archived files are saved to.
            error_dir = "ERROR_DIR_PATH"

            # Pulled Search Process/RabbitMQ Configuration section.
            user = "USER"
            pswd = "PSWD"
            host = "HOSTNAME"
            # RabbitMQ Queue name.
            queue = "QUEUENAME"
            # RabbitMQ R-Key name (normally same as queue name).
            r_key = "RKEYNAME"
            # RabbitMQ Exchange name for each instance run.
            exchange_name = "EXCHANGE_NAME"
            # RabbitMQ listening port, default is 5672.
            port = 5672
            # Type of exchange:  direct, topic, fanout, headers
            exchange_type = "direct"
            # Is exchange durable: True|False
            x_durable = True
            # Are queues durable: True|False
            q_durable = True
            # Do queues automatically delete once message is
            #   processed:  True|False
            auto_delete = False

            # Pulled Search Insert Configuration section.
            # Directory where to monitor for new files to insert into Mongodb.
            monitor_dir = "MONITOR_DIR_PATH"
            # Regular expression for search for Insert/Mongodb file names.
            mfile_regex = "_mongo.json"
            # Directory path to where Insert/Mongodb error and non-processed
            #   files are saved to.
            marchive_dir = "ARCHIVE_DIR_PATH"
            # Directory path to where Insert/Mongodb archived files are saved
            #   to.
            merror_dir = "ERROR_DIR_PATH"
            # Name of Mongo configuration file.  (Do not include the ".py"
            #   in the name.)
            # No not change unless changing the name of the external Mongo
            #   config file.
            mconfig = "mongo"

        Configuration file (config/mongo.py.TEMPLATE).  Below is the
        configuration file format for the Mongo instance setup.

            # Pulled Search Insert/Mongo DB Configuration section.
            user = "USERNAME"
            passwd = "PASSWORD"
            # Mongo DB host information
            host = "HOST_IP"
            name = "HOSTNAME"
            # Mongo database port (default is 27017)
            port = 27017
            # Mongo configuration settings
            conf_file = None
            # Authentication required:  True|False
            auth = True

            # Replica Set Mongo configuration settings.
            # Replica set name.
            #    None means the Mongo database is not part of a replica set.
            #    Example:  repset = "REPLICA_SET_NAME"
            repset = None
            # Replica host listing.
            #    None means the Mongo database is not part of a replica set.
            #    Example:  repset_hosts = "HOST1:PORT, HOST2:PORT, [...]"
            repset_hosts = None
            # Database to authentication to.
            #    Example:  db_auth = "AUTHENTICATION_DATABASE"
            db_auth = None

    Examples:
        pulled_search.py -c search -d /opt/local/pulled/config -P
            -t Mark.J.Pernot@coe.ic.gov -s Pulled Search Notification

        pulled_search.py -c search -d /opt/local/pulled/config -P
            -t Mark.J.Pernot@coe.ic.gov -s Pulled Search Notification

        pulled_search.py -c search -d /opt/local/pulled/config -I
            -n /opt/local/pulled/monitor -y pulled_insert

"""

# Libraries and Global Variables

# Standard
# For Python 2.6/2.7: Redirection of stdout in a print command.
from __future__ import print_function
import sys
import os
import socket
import getpass
import datetime
import subprocess

# Third-party
import json
import calendar
import re
import platform
import decimal

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import rabbit_lib.rabbitmq_class as rabbitmq_class
import mongo_lib.mongo_libs as mongo_libs
import checklog.check_log as check_log
import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def non_processed(docid_files, error_dir, log, mail=None, **kwargs):

    """Function:  non_processed

    Description:  Process non-processed files.

    Arguments:
        (input) docid_files -> List of files not processed.
        (input) error_dir -> Directory to move non-processed files to.
        (input) log -> Log class instance.
        (input) mail -> Mail instance.

    """

    docid_files = list(docid_files)

    if docid_files:
        log.log_info("non_processed:  Non-processed files detected.")

        for fname in docid_files:
            log.log_info("non_processed:  Moving file: %s" % (fname))
            dtg = datetime.datetime.strftime(datetime.datetime.now(),
                                             "%Y%m%d_%H%M%S")
            new_fname = os.path.basename(fname)
            gen_libs.mv_file2(fname, error_dir,
                              new_fname=new_fname + "." + dtg)

        if mail:
            log.log_info("non_processed:  Sending email...")
            mail.add_2_msg(docid_files)
            mail.send_mail()


# Look at creating a function in RabbitMQ class - setup todo item for this.
# See mail_2_rmq.create_rq for details too.
def create_rmq(cfg, q_name, r_key, **kwargs):

    """Function:  create_rmq

    Description:  Create and return a RabbitMQ Publisher instance.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) q_name -> Queue name in RabbitMQ.
        (input) r_key -> Routing key in RabbitMQ.
        (output) RabbitMQ Publisher instance.

    """

    return rabbitmq_class.RabbitMQPub(cfg.user, cfg.pswd, cfg.host, cfg.port,
                                      cfg.exchange_name, cfg.exchange_type,
                                      q_name, r_key, cfg.x_durable,
                                      cfg.q_durable, cfg.auto_delete)


# Look at creating a function in RabbitMQ class - setup todo item for this.
# See mail_2_rmq.connect_process for details too.
def send_2_rabbitmq(cfg, log_json, **kwargs):

    """Function:  send_2_rabbitmq

    Description:  Connect to RabbitMQ and publish message.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) log_json -> JSON document of log entries.
        (output) status -> True|False - Success of publishing to RabbitMQ.

    """

    rmq = create_rmq(cfg, cfg.queue, cfg.r_key)
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
        if rmq.publish_msg(log_json):
            status = True

        else:
            status = False

    else:
        status = False

    return status


def create_json(cfg, docid_dict, file_log, **kwargs):

    """Function:  create_json

    Description:  Create the JSON from the docid file and log entries.

    Arguments:
        (input) cfg -> Configuration setup.
        (input) docid_dict -> Dictionary of docid file.
        (input) file_log -> List of log file entries.
        (output) log_json -> Dictionary of docid file and log entries.

    """

    docid_dict = dict(docid_dict)
    file_log = list(file_log)
    dtg = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d %H%M%S")
    log_json = {"docID": docid_dict["docid"],
                "command": docid_dict["command"],
                "pubDate": docid_dict["pubdate"],
                "securityEnclave": cfg.enclave,
                "asOf": dtg,
                "serverName": socket.gethostname(),
                "logEntries": file_log}

    return log_json


# Move to python_libs.gen_libs module.
def month_days(dt, **kwargs):

    """Function:  month_days

    Description:  Return the number of days in the month for the date.

    Arguments:
        (input) dt -> Date, must be a datetime class instance.
        (output) -> Number of days in the month for the date.

    """

    return calendar.monthrange(dt.year, dt.month)[1]


# Move to python_libs.gen_libs module.
def date_range(start_dt, end_dt, **kwargs):

    """Function:  date_range

    Description:  Generators a list of year-month combinations between two
        dates.
        NOTE:  The day will be included in the datetime instance, but all days
            will be set to the beginning of each month (e.g. YYYY-MM-01).

    Arguments:
        (input) start_dt -> Start date - datetime class instance.
        (input) end_dt -> End date - datetime class instance.
        (output) Generator list of datetime instances.

    """

    start_dt = start_dt.replace(day=1)
    end_dt = end_dt.replace(day=1)
    forward = end_dt >= start_dt
    finish = False
    dt = start_dt

    while not finish:
        yield dt.date()

        if forward:
            days = month_days(dt)
            dt = dt + datetime.timedelta(days=days)
            finish = dt > end_dt

        else:
            _tmp_dt = dt.replace(day=1) - datetime.timedelta(days=1)
            dt = (_tmp_dt.replace(day=dt.day))
            finish = dt < end_dt


def get_archive_files(archive_dir, cmd, pubdate, cmd_regex, **kwargs):

    """Function:  get_archive_files

    Description:  Get list of archive log files.

    Arguments:
        (input) archive_dir -> Directory path to base archive logs.
        (input) cmd -> Command to search in.
        (input) pubdate -> Published date of document.
        (input) cmd_regex -> Regular expression of log file name.
        (output) log_files -> List of archive log files to search.

    """

    log_files = []
    cmd_dir = os.path.join(archive_dir, cmd)
    start_dt = datetime.datetime.strptime(pubdate[0:6], "%Y%m")
    end_dt = datetime.datetime.now() - datetime.timedelta(days=1)

    for x in date_range(start_dt, end_dt):
        yearmon = datetime.date.strftime(x, "%Y/%m")
        full_dir = os.path.join(cmd_dir, yearmon)
        log_files = log_files + dir_file_search(full_dir, cmd_regex,
                                                add_path=True)

    return log_files


# Move to python-lib.gen_libs.py.
def dir_file_search(dir_path, file_str, add_path=False, **kwargs):

    """Function:  dir_file_search

    Description:  Return a list of file names from a directory that contain
        a the search string somewhere in the name.

    NOTE:  file_str can handle regular expressions.

    Arguments:
        (input) dir_path -> Directory path to search in.
        (input) file_str -> Name of search string.
        (input) add_path -> True|False - Add path name to file name.
        (output) Return a list of (path/)file names with search string.

    """

    if add_path:
        return [os.path.join(dir_path, x)
                for x in gen_libs.list_files(dir_path)
                if re.search(file_str, x)]

    else:
        return [x for x in gen_libs.list_files(dir_path)
                if re.search(file_str, x)]


def zgrep_search(file_list, keyword, outfile, **kwargs):

    """Function:  zgrep_search

    Description:  Zgrep compressed files for keyword and write to file.

    NOTE:  This is for use on Centos 2.6.X systems and earlier.

    Arguments:
        (input) file_list -> List of files to search.
        (input) keyword -> Value to search for.
        (input) outfile -> File to write the results to.

    """

    file_list = list(file_list)
    cmd = "zgrep"

    for fname in file_list:

        with open(outfile, "ab") as fout:

            # Search for keyword and write to file.
            P1 = subprocess.Popen([cmd, keyword, fname], stdout=fout)
            P1.wait()


def process_docid(args_array, cfg, fname, log, **kwargs):

    """Function:  process_docid

    Description:  Processes the docid.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) cfg -> Configuration setup.
        (input) fname -> Docid file name.
        (input) log -> Log class instance.
        (output) status -> True|False - File has successfully processed.

    """

    args_array = dict(args_array)
    file_log = list()
    status = True
    data_list = gen_libs.file_2_list(fname)
    docid_dict = json.loads(gen_libs.list_2_str(data_list))

    # Special case exception for one command.
    if docid_dict["command"].lower() == "eucom":
        cmd = "intelink"

    else:
        cmd = docid_dict["command"].lower()

    cmd_regex = cmd + ".*" + cfg.log_type

    if args_array.get("-a", None):
        log.log_info("process_docid:  Searching for archive log files...")
        log_files = get_archive_files(cfg.archive_dir, cmd,
                                      docid_dict["pubdate"], cmd_regex)

    else:
        log.log_info("process_docid:  Searching for apache log files...")
        log_files = dir_file_search(cfg.log_dir, cmd_regex, add_path=True)

    is_centos = \
        True if "centos" in platform.linux_distribution()[0].lower() else False
    is_pre_7 = \
        decimal.Decimal(platform.linux_distribution()[1]) < \
        decimal.Decimal('7.0')

    # Must use zgrep searching in pre-Centos 7 versions.
    if is_centos and is_pre_7:
        log.log_info("process_docid:  Running zgrep search...")
        zgrep_search(log_files, docid_dict["docid"], cfg.outfile)

    else:
        # Create argument list for check_log program.
        search_args = {"-g": "w", "-f": log_files, "-S": [docid_dict["docid"]],
                       "-k": "or", "-o": cfg.outfile, "-z": True}
        log.log_info("process_docid:  Running check_log search...")
        check_log.run_program(search_args)

    if not gen_libs.is_empty_file(cfg.outfile):
        log.log_info("process_docid:  Log entries detected.")
        file_log = gen_libs.file_2_list(cfg.outfile)

    else:
        log.log_info("process_docid:  No log entries detected.")

    err_flag, err_msg = gen_libs.rm_file(cfg.outfile)

    if err_flag:
        log.log_warn("process_docid:  %s" % (err_msg))

    if file_log:
        log_json = create_json(cfg, docid_dict, file_log)
        log.log_info("process_docid:  Log entries publishing to RabbitMQ.")
        status = send_2_rabbitmq(cfg, json.dumps(log_json))

    return status


def process_insert(args_array, cfg, fname, log, **kwargs):

    """Function:  process_insert

    Description:  Process the insert file and send to a database.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) cfg -> Configuration setup.
        (input) fname -> Insert file name.
        (input) log -> Log class instance.
        (output) status -> True|False - File has successfully processed.

    """

    args_array = dict(args_array)
    log.log_info("process_insert:  Converting data to JSON.")
    data_list = gen_libs.file_2_list(fname)
    insert_dict = json.loads(gen_libs.list_2_str(data_list))

    if isinstance(insert_dict, dict):
        log.log_info("process_insert:  Inserting data into Mongodb.")
        mcfg = gen_libs.load_module(cfg.mconfig, args_array["-d"])
        mongo_libs.ins_doc(mcfg, mcfg.db, mcfg.tbl, insert_dict)
        status = True

    else:
        log.log_err("process_insert: Data failed to convert to JSON.")
        status = False

    return status


def setup_mail(args_array, subj=None, **kwargs):

    """Function:  setup_mail

    Description:  Processes the docid files.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) subj -> Email subject line.
        (output) mail -> Mail instance.

    """

    mail = None

    if args_array.get("-t", None):
        mail = gen_class.setup_mail(args_array.get("-t"),
                                    subj=args_array.get("-s", subj))

    return mail


def process_list(args_array, cfg, log, file_list, action, **kwargs):

    """Function:  process_list

    Description:  Processes the docid files.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) cfg -> Configuration setup.
        (input) log -> Log class instance.
        (input) file_list -> List of files to be processed.
        (input) action -> Type of processing to complete.
            "search" -> Execute a pulled search on the file.
            "insert" -> Insert data file into database.
        (output) done_list -> List of files successfully processed.

    """

    done_list = list()
    args_array = dict(args_array)
    file_list = list(file_list)

    for fname in file_list:
        log.log_info("process_docids:  Processing file: %s" % (fname))

        if action == "search":
            log.log_info("process_docids:  Action: search")
            status = process_docid(args_array, cfg, fname, log)

        elif action == "insert":
            log.log_info("process_docids:  Action: insert")
            status = process_insert(args_array, cfg, fname, log)

        else:
            log.log_warn("process_docids:  Incorrect or no action detected: %s"
                         % (action))
            status = False

        if status:
            done_list.append(fname)

    return done_list


def cleanup_files(docid_files, processed_list, dest_dir, log, **kwargs):

    """Function:  cleanup_files

    Description:  Send processed files to destination directory and remove
        from master file list.

    Arguments:
        (input) docid_files -> List of files to be processed.
        (input) processed_list -> List of files that were processed.
        (input) dest_dir -> Directory to move processed files to.
        (input) log -> Log class instance.
        (output) docid_files -> Modified list of files not processed.

    """

    docid_files = list(docid_files)
    processed_list = list(processed_list)

    for fname in processed_list:
        log.log_info("cleanup_files:  Archiving file: %s" % (fname))
        dtg = datetime.datetime.strftime(datetime.datetime.now(),
                                         "%Y%m%d_%H%M%S")
        new_fname = os.path.basename(fname)
        gen_libs.mv_file2(fname, dest_dir, new_fname=new_fname + "." + dtg)
        docid_files.remove(fname)

    return docid_files


def process_files(args_array, cfg, log, **kwargs):

    """Function:  process_files

    Description:  Processes the docid files.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) cfg -> Configuration setup.
        (input) log -> Log class instance.

    """

    args_array = dict(args_array)
    mail = setup_mail(args_array, subj="Non-processed files")
    log.log_info("process_files:  Processing files to search...")
    docid_files = dir_file_search(cfg.doc_dir, cfg.file_regex, add_path=True)
    remove_list = process_list(args_array, cfg, log, docid_files, "search")
    docid_files = cleanup_files(docid_files, remove_list, cfg.archive_dir, log)
    non_processed(docid_files, cfg.error_dir, log, mail)


def insert_data(args_array, cfg, log, **kwargs):

    """Function:  insert_data

    Description:  Insert pulled search files into Mongodb.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) cfg -> Configuration setup.
        (input) log -> Log class instance.

    """

    args_array = dict(args_array)
    log.log_info("insert_data:  Processing files to insert...")
    insert_list = dir_file_search(cfg.monitor_dir,
                                  cfg.mfile_regex, add_path=True)
    remove_list = process_list(args_array, cfg, log, insert_list, "insert")
    insert_list = cleanup_files(insert_list, remove_list, cfg.marchive_dir,
                                log)
    mail = setup_mail(args_array, subj="Non-processed files")
    non_processed(insert_list, cfg.merror_dir, log, mail)


def validate_dirs(cfg, **kwargs):

    """Function:  validate_dirs

    Description:  Validate the directories in the configuration file for the
        -P option.

    Arguments:
        (input) cfg -> Configuration setup.
        (output) msg_dict -> Dictionary of any error messages detected.

    """

    msg_dict = dict()

    status, msg = gen_libs.chk_crt_dir(cfg.doc_dir, write=True, no_print=True)

    if not status:
        msg_dict[cfg.doc_dir] = msg

    status, msg = gen_libs.chk_crt_dir(cfg.log_dir, read=True, no_print=True)

    if not status:
        msg_dict[cfg.log_dir] = msg

    basepath = gen_libs.get_base_dir(cfg.outfile)
    status, msg = gen_libs.chk_crt_dir(basepath, write=True, create=True,
                                       no_print=True)

    if not status:
        msg_dict[basepath] = msg

    status, msg = gen_libs.chk_crt_dir(cfg.error_dir, write=True, create=True,
                                       no_print=True)

    if not status:
        msg_dict[cfg.error_dir] = msg

    status, msg = gen_libs.chk_crt_dir(cfg.archive_dir, write=True,
                                       create=True, no_print=True)

    if not status:
        msg_dict[cfg.archive_dir] = msg

    return msg_dict


def mvalidate_dirs(cfg, **kwargs):

    """Function:  mvalidate_dirs

    Description:  Validate the directories in the configuration file for the
        -I option.

    Arguments:
        (input) cfg -> Configuration setup.
        (output) msg_dict -> Dictionary of any error messages detected.

    """

    msg_dict = dict()

    status, msg = gen_libs.chk_crt_dir(cfg.monitor_dir, write=True,
                                       no_print=True)

    if not status:
        msg_dict[cfg.monitor_dir] = msg

    status, msg = gen_libs.chk_crt_dir(cfg.merror_dir, write=True, create=True,
                                       no_print=True)

    if not status:
        msg_dict[cfg.merror_dir] = msg

    status, msg = gen_libs.chk_crt_dir(cfg.marchive_dir, write=True,
                                       create=True, no_print=True)

    if not status:
        msg_dict[cfg.marchive_dir] = msg

    return msg_dict


def checks_dirs(args_array, cfg, **kwargs):

    """Function:  checks_dirs

    Description:  Validate the directories in the configuration file depending
        on the options selected.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) cfg -> Configuration setup.
        (output) msg_dict -> Dictionary of any error messages detected.

    """

    args_array = dict(args_array)
    msg_dict = dict()

    if args_array.get("-P", None):
        msg_dict = validate_dirs(cfg)

    elif args_array.get("-I", None):
        msg_dict = mvalidate_dirs(cfg)

    return msg_dict


def config_override(args_array, cfg, **kwargs):

    """Function:  config_override

    Description:  Checks for specific arguments which will override the
        values for some configuration settings.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) cfg -> Configuration setup.
        (output) cfg -> Modified configuration setup.

    """

    if args_array.get("-m", None):
        cfg.doc_dir = args_array["-m"]

    if args_array.get("-n", None):
        cfg.monitor_dir = args_array["-n"]

    return cfg


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Controls the running of the program by loading and
        validating the configuration file and calling the function to
        process the docid files.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) func_dict -> Dict of function calls for different options.

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)
    cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])
    basepath = gen_libs.get_base_dir(cfg.log_file)
    status, err_msg = gen_libs.chk_crt_dir(basepath, write=True, create=True,
                                           no_print=True)

    if status:
        log = gen_class.Logger(cfg.log_file, cfg.log_file, "INFO",
                               "%(asctime)s %(levelname)s %(message)s",
                               "%Y-%m-%dT%H:%M:%SZ")
        log.log_info("Program initialization...")
        cfg = config_override(args_array, cfg)
        msg_dict = checks_dirs(args_array, cfg)

        if msg_dict:
            log.log_err("Validation of configuration directories failed")
            log.log_err("Message: %s" % (msg_dict))
            mail = gen_class.setup_mail(cfg.admin_email,
                                        subj="Directory Check Failure")
            mail.add_2_msg(msg_dict)
            mail.send_mail()

        else:
            # Determine which functions to call.
            for opt in set(args_array.keys()) & set(func_dict.keys()):
                func_dict[opt](args_array, cfg, log)

    else:
        mail = gen_class.setup_mail(cfg.admin_email,
                                    subj="Logger Directory Check Failure")
        mail.add_2_msg(err_msg)
        mail.send_mail()


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        func_dict -> dictionary of function calls for different options.
        opt_con_req_dict -> contains options requiring other options.
        opt_multi_list -> contains the options that will have multiple values.
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.
        opt_xor_dict -> contains dict with key that is xor with it's values.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    dir_chk_list = ["-d", "-m", "-n"]
    func_dict = {"-P": process_files, "-I": insert_data}
    opt_con_req_dict = {"-s": ["-t"]}
    opt_multi_list = ["-s", "-t"]
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d", "-m", "-n", "-s", "-t", "-y"]
    opt_xor_dict = {"-I": ["-P"], "-P": ["-I"]}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list,
                                       multi_val=opt_multi_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_cond_req_or(args_array, opt_con_req_dict) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list) \
       and arg_parser.arg_xor_dict(args_array, opt_xor_dict):

        try:
            prog_lock = gen_class.ProgramLock(sys.argv,
                                              args_array.get("-y", ""))
            run_program(args_array, func_dict)
            del prog_lock

        except gen_class.SingleInstanceException:
            print("WARNING:  Lock in place for pulled_search with id of: %s"
                  % (args_array.get("-y", "")))


if __name__ == "__main__":
    sys.exit(main())
