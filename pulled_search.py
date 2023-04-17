#!/usr/bin/python
# Classification (U)

"""Program:  pulled_search.py

    Description:  The pulled_search program is a multi-optional program for use
        with the pulled product process.  It can detect when new pulled product
        files are created, parse the file, call the search program to check log
        files for the docid in the file.  Any entries found will be converted
        into a JSON document and send to a RabbitMQ queue.  The program also
        has the ability to detect when new search pulled product log entries
        are available to be inserted into a database.  The program now has the
        the ability to search for docids listed in a file.

    Usage:
        pulled_search.py -c file -d path
            {-P [-m path] [-a] [-i] |
             -F /path/filename [-a] [-i] |
             -I [-n path]}
            [-t email {email2 email3 ...} {-s subject_line}]
            [-y flavor_id]
            [-v | -h]

    Arguments:
        -c file => Configuration file.  Required argument.
        -d dir_path => Directory path for option '-c'.  Required argument.

        -P => Process Doc ID files send to RabbitMQ.
            -i => Insert the log entries directly to Mongodb.
            -m dir_path => Directory to monitor for doc ID files.
            -a => This is an archive log search.

        -F /path/filename => Process DocIDs from a file.
            -i => Insert the log entries directly to Mongodb.
            -a => This is an archive log search.

        -I => Insert Pulled Search files into Mongodb.
            -n dir_path => Directory to monitor for pulled search files.

        -t email_address(es) => Send output to one or more email addresses.
            -s subject_line => Pre-amble to the subject line of email.

        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        WARNING 1:  -a option must be used for archive log searching otherwise
            the incorrect servername will be set in the JSON document.

        NOTE 1:  -v or -h overrides the other options.
        NOTE 2:  -t option is for reporting any errors detected.
        NOTE 3:  -s requires -t option to be included.
        NOTE 4:  -P, -F and -I are XOR options.
        NOTE 5:  -m and -n options will override the configuration settings.
            The -m option is mapped to the doc_dir configuration entry, and
            the -n option is mapped to the monitor_dir configuration entry.
        NOTE 6:  The log files can be normal flat files or compressed files
            (e.g. ending with .gz) or a combination there of.  Any other type
            of compressed file will not work.
        NOTE 7: -i option overrides sending the JSON document to RabbitMQ
            directly or via email.

    Input files:
        The file for the -F option must be in the following layout in ACSII
        format.  The fields are space-delimited.
        Each line of the file consists of three fields:
            docid command publication_date
        Example:
            09109abcdef EUCOM 20230417

    Configuration files:
        Configuration file (config/search.py.TEMPLATE).  Below is the
        configuration file format for the environment setup in the program.

        # Pulled Search General Configuration section.
        # This section is for either the -P or -I option.
        #
        # Logger file for the storage of log entries.
        # File name including directory path.
        log_file = "BASE_PATH/log/pulled_search.log"

        # Pulled Search Process Configuration section.
        # Update this section if using the -P option.
        #
        # Directory where Docid Pulled Html files are located at.
        # NOTE: Do not include the YYYY/MM as part of the path as this will be
        #   added.
        doc_dir = ["DOC_DIR_PATH", "DOC_DIR_PATH2"]
        # Path and file name for previous processed files.
        processed_file = "BASE_PATH/processed/processed"
        # Regular expression for search for log file names.
        file_regex = "-PULLED-"
        # Regular expression for search for recalled products.
        pattern = "JAC.pull.subtype.*.SECURITY RECALL"

        # Enter the archive_log_dir if using the -a option otherwise enter the
        #   log_dir.
        # Directory where active log files to be searched are.
        log_dir = "LOG_DIR_PATH"
        # Directory where archived log files to be searched are.
        archive_log_dir = "ARCHIVE_DIR_PATH"

        # Type of log files to checked.
        log_type = "access_log"
        # Temporary file where check_log will write to.
        # File name including directory path.
        outfile = "BASE_PATH/tmp/checklog.out"
        # Security enclave these files are being processed on.
        enclave = "ENCLAVE"
        # Directory path to where error and non-processed files are saved to.
        error_dir = "BASE_PATH/search_error"
        # Mapping of commands to keywords.
        # This is for the naming of the access logs which are not always under
        #   the command name.
        command = {"intelink": "eucom"}

        # Pulled Search Process/RabbitMQ Configuration section.
        # Update this section if using the -P option.
        # Fill either the mail section to send to RabbitMQ via email or fill in
        #   the RabbitMQ section to publish to RabbitMQ directly.  If using
        #   mail option this is normally used in conjunction with the
        #   rmq_2_mail.py program.
        # Note: If the email is filled in then this will override the RabbitMQ
        #   section.
        #
        # Email section
        # Email address to rabbitmq alias for the rmq_2_mail.py program.
        #   Note:  Leave to_addr and subj set to None if not using email
        #   capability.
        # Example: to_addr = "rabbitmq@domain.name"
        to_addr = None
        # Name of the RabbitMQ queue.
        # Note: Subject must match exactly the RabbitMQ queue name and is
        #   case-sensitive.
        # Example:  subj = "Pulledsearch"
        subj = None
        #
        # RabbitMQ section
        # Login information.
        user = "USER"
        japd = "PSWORD"
        # Address to single RabbitMQ node.
        host = "HOSTNAME"
        # List of hosts along with their ports to a multiple node RabbitMQ
        #   cluster.
        # Format of each entry is: "IP:PORT".
        # Example:
        #   host_list = ["hostname:5672", "hostname2:5672", "hostname:5673"]
        # Note:  If host_list is set, it will take precedence over the host
        #   entry.
        host_list = []
        # RabbitMQ Queue name.
        queue = "QUEUENAME"
        # RabbitMQ R-Key name (normally same as queue name).
        r_key = "RKEYNAME"
        # RabbitMQ Exchange name for each instance run.
        exchange_name = "EXCHANGE_NAME"
        # RabbitMQ listening port
        # Default is 5672
        port = 5672
        # Type of exchange
        # Names allowed:  direct, topic, fanout, headers
        exchange_type = "direct"
        # Is exchange durable: True|False
        x_durable = True
        # Are queues durable: True|False
        q_durable = True
        # Do queues automatically delete once message is processed:  True|False
        auto_delete = False

        # Pulled Search Insert Configuration section.
        # Update this section if using the -I option.
        # Directory where to monitor for new files to insert into Mongodb.
        monitor_dir = "MONITOR_DIR_PATH"
        # Regular expression for search for Insert/Mongodb file names.
        mfile_regex = "_mongo.json"
        # Directory path to where Insert/Mongodb archived files are saved to.
        marchive_dir = "BASE_PATH/archive"
        # Directory path to where Insert/Mongodb error and non-processed files
        #   are saved to.
        merror_dir = "BASE_PATH/mongo_error"
        # Name of Mongo configuration file.  (Do not include the ".py" in the
        #   name.)
        # Do not change unless changing the name of the external Mongo config
        #   file.
        mconfig = "mongo"

        # Log parsing section.
        # Warning: Do not modify this section unless you know regular
        #   expressions.
        # NOTE: These name tags are reserved and cannot be used:
        #   ["command", "docid", "network", "pubDate", "asOf"]
        regex = "(?P<ip>.*?) (?P<proxyid>.*?) (?P<userid>.*?)
            \[(?P<logTime>.*?)(?= ) (?P<timeZone>.*?)\] (?P<requestid>.*?)
            (?P<secs>.*?)/(?P<msecs>.*?) \"(?P<verb>.*?)
            HTTP/(?P<httpVer>.*?)\" (?P<status>.*?) (?P<length>.*?)
            \"(?P<referrer>.*?)\" \"(?P<userAgent>.*?)\" (?P<url>.*?)?$"
        # These are the entries that will be parsed from the log entry and
        #   placed into the document.
        # Note: Name tags must match between regex and allowable and are
        #   case-sensitive.
        allowable = ["userid", "logTime", "verb", "status", "url"]

        Mongo configuration file format (config/mongo.py.TEMPLATE).  The
        configuration file format is for connecting to a Mongo database or
        replica set for monitoring.  A second configuration file can also
        be used to connect to a Mongo database or replica set to insert the
        results of the performance monitoring into.

        # Pulled Search Insert/Mongo DB Configuration section.
        # Update this file if using the -I option.
        user = "USER"
        japd = "PSWORD"
        # Mongo DB host information
        host = "HOST_IP"
        name = "HOSTNAME"
        # Mongo database port
        # Default port for Mongo is 27017.
        port = 27017
        # Mongo configuration settings
        # Only set if using a different Mongo configuration file.
        conf_file = None
        # Authentication required:  True|False
        # Only set to False if no authentication is taking place.
        auth = True
        # Authentication database
        # Name of database to authenticate the user in.
        auth_db = "admin"
        # Authentication mechanism
        #   Current values allowed:  MONGODB-CR, SCRAM-SHA-1, SCRAM-SHA-256
        #   NOTE 1:  SCRAM-SHA-256 only works for Mongodb 4.0 and better.
        #   NOTE 2:  FIPS 140-2 environment requires SCRAM-SHA-1 or
        #       SCRAM-SHA-256.
        #   NOTE 3:  MONGODB-CR is not suppoerted in Mongodb 4.0 and better.
        auth_mech = "SCRAM-SHA-1"

        # Replica Set Mongo configuration settings.
        # By default all settings are set to None.
        #    None means the Mongo database is not part of a replica set.
        #
        # Replica set name.
        # Format:  repset = "REPLICA_SET_NAME"
        repset = None
        # Replica host listing.
        # Format:  repset_hosts = "HOST1:PORT, HOST2:PORT, [...]"
        repset_hosts = None
        # Database to authentication to.
        # Format:  db_auth = "AUTHENTICATION_DATABASE"
        db_auth = None

        # SSL Configuration settings
        # If not set will connect to Mongo without using SSL connections.
        # File containing the SSL certificate authority.
        # Example: ssl_client_ca = "/opt/mongo/certs/ca.pem"
        ssl_client_ca = None
        # File containing the SSL key.
        # Example:  ssl_client_key = "/opt/mongo/certs/client-key.pem"
        ssl_client_key = None
        # File containing the SSL certificate file.
        # Example: ssl_client_cert = "/opt/mongo/certs/client-cert.pem"
        ssl_client_cert = None
        # Pass phrase for the SSL Client Key, if one is set.
        # Example:  ssl_client_phrase = "Phrase"
        ssl_client_phrase = None

        # Name of Mongo database for data insertion
        dbs = "DATABASE"
        # Name of Mongo collection
        tbl = "COLLECTION"

        Configuration modules -> Name is runtime dependent as it can be used to
            connect to different databases with different names.

    Examples:
        pulled_search.py -c search -d /opt/local/pulled/config -P
            -t myname@email.domain -s Pulled Search Notification

        pulled_search.py -c search -d /opt/local/pulled/config -I
            -n /opt/local/pulled/monitor -y pulled_insert

"""

# Libraries and Global Variables
from __future__ import print_function
from __future__ import absolute_import

# Standard
import sys
import os
import socket
import datetime
import json
import re

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .rabbit_lib import rabbitmq_class
    from .mongo_lib import mongo_libs
    from .checklog import check_log
    from . import version

except (ValueError, ImportError) as err:
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


def non_processed(docid_files, error_dir, log, mail=None):

    """Function:  non_processed

    Description:  Process non-processed files.

    Arguments:
        (input) docid_files -> List of files not processed
        (input) error_dir -> Directory to move non-processed files to
        (input) log -> Log class instance
        (input) mail -> Mail instance

    """

    log.log_info("non_processed:  Post-process of files.")
    docid_files = list(docid_files)

    if docid_files:
        log.log_info("non_processed:  Non-processed files detected.")

        for fname in docid_files:
            log.log_info("non_processed:  File: %s moved to %s"
                         % (fname, error_dir))
            dtg = datetime.datetime.strftime(
                datetime.datetime.now(), "%Y%m%d_%H%M%S")
            new_fname = os.path.basename(fname)
            gen_libs.mv_file2(
                fname, error_dir, new_fname=new_fname + "." + dtg)

        if mail:
            log.log_info("non_processed:  Send email of non-processed file.")
            mail.add_2_msg(docid_files)
            mail.send_mail()


def get_archive_files(archive_dir, cmd, pubdate, cmd_regex):

    """Function:  get_archive_files

    Description:  Get list of archive log files.

    Arguments:
        (input) archive_dir -> Directory path to base archive logs
        (input) cmd -> Command to search in
        (input) pubdate -> Published date of document
        (input) cmd_regex -> Regular expression of log file name
        (output) log_files -> List of archive log files to search

    """

    log_files = []
    cmd_dir = os.path.join(archive_dir, cmd)
    start_dt = datetime.datetime.strptime(pubdate[0:6], "%Y%m")
    end_dt = datetime.datetime.now() - datetime.timedelta(days=1)

    for date in gen_libs.date_range(start_dt, end_dt):
        yearmon = datetime.date.strftime(date, "%Y/%m")
        full_dir = os.path.join(cmd_dir, yearmon)
        log_files = log_files + gen_libs.filename_search(
            full_dir, cmd_regex, add_path=True)

    return log_files


def process_docid(args, cfg, docid_dict, log):

    """Function:  process_docid

    Description:  Processes the docid.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) docid_dict -> Dictionary containing docid information
        (input) log -> Log class instance
        (output) status -> True|False - File has successfully processed

    """

    status = True
    docid_dict = dict(docid_dict)
    log.log_info("process_docid:  Processing docid: %s" % (docid_dict))
    cmd = docid_dict["command"].lower()
    server = socket.gethostname()

    # Check to see if the command is mapped to a different keyword file
    if cmd in cfg.command:
        cmd = cfg.command[cmd]

    cmd_regex = cmd + ".*" + cfg.log_type

    if args.arg_exist("-a"):
        log.log_info("process_docid:  Searching archive directory: %s"
                     % (cfg.archive_log_dir))
        log_files = get_archive_files(
            cfg.archive_log_dir, cmd, docid_dict["pubdate"], cmd_regex)

    else:
        log.log_info("process_docid:  Searching apache log directory: %s"
                     % (cfg.log_dir))
        log_files = gen_libs.filename_search(
            cfg.log_dir, cmd_regex, add_path=True)

    dtg = datetime.datetime.strftime(
        datetime.datetime.now(), "%Y-%m-%dT%H:%M:%SZ")
    log_json = {"docid": docid_dict["docid"],
                "command": docid_dict["command"],
                "pubDate": docid_dict["pubdate"],
                "network": cfg.enclave,
                "asOf": dtg, "servers": dict()}
    log.log_info("process_docid:  Running check_log search.")

    for fname in log_files:

        if args.arg_exist("-a"):
            data = fname.split(".")
            server = data[-2] if data[-1] == "gz" else data[-1]

        ofile = cfg.outfile + datetime.datetime.strftime(
            datetime.datetime.now(), "%Y%m%d%H%M%S")
        cmdline = [
            "check_log.py", "-g", "w", "-f", fname, "-S",
            [docid_dict["docid"]], "-k", "or", "-o", ofile, "-z"]
        chk_opt_val = ["-g", "-f", "-S", "-k", "-o"]
        multi_val = ["-f"]
        chk_args = gen_class.ArgParser(
            cmdline, opt_val=chk_opt_val, multi_val=multi_val, do_parse=True)
        check_log.run_program(chk_args)

        if os.path.exists(ofile) and not gen_libs.is_empty_file(ofile):
            log.log_info(
                "process_docid:  Log entries detected in: %s." % (fname))
            file_log = gen_libs.file_2_list(ofile)

            log_json["servers"][server] = \
                log_json["servers"][server] + file_log \
                if server in log_json["servers"] else file_log

        if os.path.exists(ofile):
            err_flag, err_msg = gen_libs.rm_file(ofile)

            if err_flag:
                log.log_warn("process_docid:  %s" % (err_msg))

    status = process_json(args, cfg, log, log_json)

    return status


def insert_mongo(args, cfg, log, data):

    """Function:  insert_mongo

    Description:  Insert JSON document into Mongo database.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance
        (input) log_json -> JSON log document
        (output) status -> True|False - Successful insertion into Mongo

    """

    status = True
    mcfg = gen_libs.load_module(cfg.mconfig, args.get_val("-d"))
    mongo_stat = mongo_libs.ins_doc(mcfg, mcfg.dbs, mcfg.tbl, data)

    if not mongo_stat[0]:
        log.log_err("insert_mongo:  Insertion into Mongo failed.")
        log.log_err("Mongo error message:  %s" % (mongo_stat[1]))
        status = False

    return status


def parse_data(args, cfg, log, log_json):

    """Function:  parse_data

    Description:  Parse data prior to inserting into Mongo database.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance
        (input) log_json -> JSON log document
        (output) status -> True|False - Successful insertion into Mongo

    """

    log.log_info("parse_data:  Start parsing JSON document.")
    status = True
    first_stage = dict()
    first_stage["command"] = log_json["command"]
    first_stage["docid"] = log_json["docid"]
    first_stage["network"] = log_json["network"]
    first_stage["pubDate"] = log_json["pubDate"]
    first_stage["asOf"] = log_json["asOf"]
    second_stage = dict(first_stage)
    log.log_info("parse_data:  Parsing docid: %s" % (first_stage["docid"]))

    # Loop on servers
    for svr in log_json["servers"]:
        second_stage["server"] = svr
        third_stage = dict(second_stage)

        # Loop on log entries for each server
        for line in log_json["servers"][svr]:
            third_stage["entry"] = line
            parsed_line = re.match(cfg.regex, line)

            # Parse the log entry
            if parsed_line:
                parsed_line = parsed_line.groupdict()

                for entry in parsed_line:

                    if entry in cfg.allowable and entry == "url":
                        third_stage[entry] = "https://" + parsed_line[entry]

                    elif entry in cfg.allowable:
                        third_stage[entry] = parsed_line[entry]

            else:
                log.log_err("parse_data:  Unable to parse log entry: %s."
                            % (third_stage))
                log.log_warn("parse_data: Insert into Mongo without parsing.")

            status = status & insert_mongo(args, cfg, log, third_stage)
            third_stage = dict(second_stage)

        second_stage = dict(first_stage)

    return status


def process_json(args, cfg, log, log_json):

    """Function:  process_json

    Description:  Process the JSON document from the pulled search results.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance
        (input) log_json -> JSON log document
        (output) status -> True|False - Successful processing

    """

    log.log_info("process_json:  Processing JSON document.")
    status = True

    if args.arg_exist("-i"):
        log.log_info("process_json:  Inserting JSON log entries into Mongo")
        status = parse_data(args, cfg, log, log_json)

    elif cfg.to_addr and cfg.subj:
        log.log_info("process_json:  Emailing JSON log entries to: %s"
                     % (cfg.to_addr))
        mail = gen_class.setup_mail(cfg.to_addr, subj=cfg.subj)
        mail.add_2_msg(log_json)
        mail.send_mail()

    else:
        log.log_info("process_json:  Publishing log entries to RabbitMQ.")
        status, err_msg = rabbitmq_class.pub_2_rmq(
            cfg, json.dumps(log_json))

        if status:
            log.log_info("process_json:  Log entries published to RabbitMQ.")

        else:
            log.log_err(
                "process_json:  Error detected during publication.")
            log.log_err("process_json:  Message: %s" % (err_msg))
            dtg = datetime.datetime.strftime(
                datetime.datetime.now(), "%Y%m%d_%H%M%S")
            name = "NonPublished." + log_json["docid"] + "." + dtg
            fname = os.path.join(cfg.error_dir, name)
            log.log_err("process_json:  Writing JSON document to file: %s"
                        % (fname))
            gen_libs.write_file(fname, mode="w", data=log_json)

            if args.get_val("-t", def_val=False):
                log.log_info("process_json:  Email error to: %s"
                             % (args.get_val("-t")))
                subj = args.get_val("-s", def_val="") + "Error: NonPublished"
                mail = gen_class.setup_mail(args.get_val("-t"), subj=subj)
                mail.add_2_msg("Unable to publish message to RabbitMQ")
                mail.add_2_msg("File: " + fname)
                mail.send_mail()

    return status


def process_insert(args, cfg, fname, log):

    """Function:  process_insert

    Description:  Process the insert file and send to a database.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) fname -> Insert file name
        (input) log -> Log class instance
        (output) status -> True|False - File has successfully processed

    """

    log.log_info("process_insert:  Converting data to JSON.")
    status = True
    data_list = gen_libs.file_2_list(fname)
    log_json = json.loads(gen_libs.list_2_str(data_list))

    if isinstance(log_json, dict):
        status = parse_data(args, cfg, log, log_json)

    else:
        log.log_err("process_insert: Data failed to convert to JSON.")
        status = False

    return status


def cleanup_files(docid_files, processed_list, dest_dir, log):

    """Function:  cleanup_files

    Description:  Send processed files to destination directory and remove
        from master file list.

    Arguments:
        (input) docid_files -> List of files to be processed
        (input) processed_list -> List of files that were processed
        (input) dest_dir -> Directory to move processed files to
        (input) log -> Log class instance
        (output) docid_files -> Modified list of files not processed

    """

    log.log_info("cleanup_files:  Post-cleanup of files.")
    docid_files = list(docid_files)
    processed_list = list(processed_list)

    for fname in processed_list:
        log.log_info("cleanup_files:  Archiving file: %s" % (fname))
        dtg = datetime.datetime.strftime(
            datetime.datetime.now(), "%Y%m%d_%H%M%S")
        new_fname = os.path.basename(fname)
        gen_libs.mv_file2(fname, dest_dir, new_fname=new_fname + "." + dtg)
        docid_files.remove(fname)

    return docid_files


def load_processed(processed_fname):

    """Function:  load_processed

    Description:  Read in the previous processed docids.

    Arguments:
        (input) processed_fname -> Name of processed file
        (output) processed_docids -> List of processed docids

    """

    try:
        with open(processed_fname) as fhdr:
            processed_docids = [line.rstrip() for line in fhdr.readlines()]

    except IOError as msg:
        if msg.args[1] == "No such file or directory":
            processed_docids = list()

    return processed_docids


def update_processed(log, processed_fname, file_dict):

    """Function:  update_processed

    Description:  Update the processed file with new file entries.

    Arguments:
        (input) log -> Log class instance
        (input) processed_fname -> Name of processed file
        (input) file_dict -> Dictionary list of new files processed

    """

    log.log_info("update_processed:  Updating processed file: %s"
                 % (processed_fname))
    file_dict = dict(file_dict)

    with open(processed_fname, "a") as fhdr:
        for item in file_dict:
            fhdr.write(item + "\n")


def process_failed(args, cfg, log, failed_dict):

    """Function:  process_failed

    Description:  Process the failed files.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance
        (input) failed_dict -> Dictionary list of failed files

    """

    log.log_info("process_failed:  Processing failed entries.")
    dtg = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M%S")
    failed_file = os.path.join(cfg.error_dir, "failed_process." + dtg)

    with open(failed_file, "a") as fhdr:
        fhdr.write(json.dumps(failed_dict, indent=4))

    # Send email if set
    if args.get_val("-t", def_val=False):
        subj = args.get_val("-s", def_val="") + " Process failed files"
        mail = gen_class.setup_mail(args.get_val("-t"), subj=subj)
        mail.add_2_msg(json.dumps(failed_dict, indent=4))
        mail.send_mail()


def search_docid(args, cfg, docid_dict, log):

    """Function:  search_docid

    Description:  Call the process_docid and check on status of docid.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) docid_dict -> Dictionary of individual docid
        (input) log -> Log class instance
        (output) docid_status -> Dictionary of status of docid processing

    """

    docid_status = dict()
    status = process_docid(args, cfg, docid_dict, log)

    if not status:
        log.log_err("search_docid: Error detected for docid: %s"
                    % (docid_dict))
        docid_status[docid_dict["docid"]] = "Failed the process_docid process"

    return docid_status


def remove_processed(cfg, log, file_dict):

    """Function:  remove_processed

    Description:  Removes any previous processed docids from the file_dict.

    Arguments:
        (input) cfg -> Configuration setup
        (input) log -> Log class instance
        (input) file_dict -> Dictionary list of docids
        (output) file_dict -> Dict list of docids, processed docids removed

    """

    file_dict = dict(file_dict)
    log.log_info("remove_processed:  Removing previous processed docids.")
    processed_docids = load_processed(cfg.processed_file)

    for p_docids in processed_docids:
        if p_docids in file_dict:
            file_dict.pop(p_docids)

    return file_dict


def recall_search(args, cfg, log, file_dict):

    """Function:  recall_search

    Description:  Search for security recalled products in the pulled files
        and process those files.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance
        (input) file_dict -> Dictionary list of new pulled files to process
        (output) failed_dict -> Dictionary list of files that failed to process

    """

    log.log_info("recall_search:  Processing new pulled files.")
    lines = list()
    docid_dict = dict()
    failed_dict = dict()
    file_dict = dict(file_dict)

    for docid in file_dict:
        log.log_info("recall_search:  Docid: %s File: %s"
                     % (docid, file_dict[docid]))
        try:
            with open(file_dict[docid], "r") as fhdr:
                data = fhdr.readlines()
                lines = [line.rstrip() for line in data]

        except IOError as msg:
            log.log_err("recall_search: Failed to open file!")
            failed_dict[docid] = msg.args[1]
            lines = list()

        if lines:
            log.log_info("recall_search:  Searching for security recall.")

        for line in lines:
            if re.search(cfg.pattern, line):
                fname = os.path.basename(file_dict[docid])
                docid_dict["command"] = fname.split("-")[0]
                docid_dict["pubdate"] = re.split(
                    r"-|\.", fname)[re.split(
                        r"-|\.", fname).index('PULLED') + 1]
                docid_dict["docid"] = docid
                break

        if docid_dict:
            log.log_info("recall_search:  Security recall product found in: %s"
                         % (file_dict[docid]))
            failed_dict.update(search_docid(args, cfg, docid_dict, log))
            docid_dict = dict()

    return failed_dict


def recall_search2(args, cfg, log, docid_dict):

    """Function:  recall_search2

    Description:  Get docids from an input file and process the docids.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance
        (input) docid_dict -> Dictionary of docids to process
        (output) failed_dict -> Dictionary of docids that failed to process

    """

    docid_dict = dict(docid_dict)
    t_docid = dict()
    failed_dict = dict()

    for docid in docid_dict:
        log.log_info("recall_search2:  Processing docid: %s" % (docid))
        t_docid["docid"] = docid
        t_docid["command"] = docid_dict[docid]["command"]
        t_docid["pubdate"] = docid_dict[docid]["pubdate"]
        failed_dict.update(search_docid(args, cfg, t_docid, log))
        t_docid = dict()

    return failed_dict


def process_files(args, cfg, log):

    """Function:  process_files

    Description:  Processes the docid files.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance

    """

    log.log_info("process_files:  Locating pulled files.")
    docid_files = list()
    yearmon = datetime.date.strftime(datetime.datetime.now(), "%Y/%m")
    search_dir = list()

    if args.get_val("-m", def_val=None):
        search_dir.append(args.get_val("-m"))

    else:
        for dir_entry in cfg.doc_dir:
            search_dir.append(os.path.join(dir_entry, yearmon))

    for docdir in search_dir:
        log.log_info("process_files:  Searching directory: %s" % (docdir))
        tmp_list = gen_libs.filename_search(
            docdir, cfg.file_regex, add_path=True)
        docid_files.extend(tmp_list)

    log.log_info("process_files:  Removing duplicate pulled docids.")
    file_dict = {}

    for filename in docid_files:
        docid = re.split(
            r"-|\.", os.path.basename(filename))[
                re.split(r"-|\.", filename).index('html') - 1]

        if docid not in file_dict:
            file_dict[docid] = filename

    file_dict = remove_processed(cfg, log, file_dict)
    failed_dict = recall_search(args, cfg, log, file_dict)

    if file_dict:
        update_processed(log, cfg.processed_file, file_dict)

    if failed_dict:
        process_failed(args, cfg, log, failed_dict)


def file_input(args, cfg, log):

    """Function:  file_input

    Description:  Process docids via input file.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance

    """

    log.log_info("file_input:  Processing docids from input file.")
    docid_dict = dict()
    file_list = gen_libs.file_2_list(args.get_val("-F"))

    for line in file_list:
        docid = line.split(" ")[0]
        metadata = {
            "command": line.split(" ")[1], "pubdate": line.split(" ")[2]}

        if docid not in docid_dict:
            docid_dict[docid] = metadata

        else:
            log.log_warn("file_input: Duplicate lines detected in file.")
            log.log_warn("Docid: %s" % (docid))
            log.log_want("Line 1: %s" % (docid_dict[docid]))
            log.log_want("Line 2: %s" % (metadata))

    docid_dict = remove_processed(cfg, log, docid_dict)
    failed_dict = recall_search2(args, cfg, log, docid_dict)

    if docid_dict:
        update_processed(log, cfg.processed_file, docid_dict)

    if failed_dict:
        process_failed(args, cfg, log, failed_dict)


def insert_data(args, cfg, log):

    """Function:  insert_data

    Description:  Insert pulled search files into Mongodb.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance

    """

    log.log_info("insert_data:  Processing files to insert.")
    processed_list = list()
    mail = None

    if args.get_val("-t", def_val=False):
        subj = args.get_val("-s", def_val="") + "Non-processed files"
        mail = gen_class.setup_mail(args.get_val("-t"), subj=subj)

    log.log_info("insert_data:  Searching for new files.")
    insert_list = gen_libs.filename_search(
        cfg.monitor_dir, cfg.mfile_regex, add_path=True)

    for fname in insert_list:
        log.log_info("insert_data:  Processing file: %s" % (fname))
        status = process_insert(args, cfg, fname, log)

        if status:
            processed_list.append(fname)

    if insert_list:
        log.log_info("insert_data:  Post-processing of files.")
        nonproc_list = cleanup_files(
            insert_list, processed_list, cfg.marchive_dir, log)
        non_processed(nonproc_list, cfg.merror_dir, log, mail)


def validate_dirs(cfg, args):

    """Function:  validate_dirs

    Description:  Validate the directories in the configuration file for the
        -P option.

    Arguments:
        (input) cfg -> Configuration setup
        (input) args -> ArgParser class instance
        (output) msg_dict -> Dictionary of any error messages detected

    """

    msg_dict = dict()

    # Directory where Docid Pulled Html files are located at
    for entry in cfg.doc_dir:
        status, msg = gen_libs.chk_crt_dir(entry, read=True, no_print=True)

        if not status:
            msg_dict[entry] = msg

    if args.get_val("-a", def_val=None):
        # Directory path to where archived log files to be searched are
        status, msg = gen_libs.chk_crt_dir(
            cfg.archive_log_dir, read=True, no_print=True)

        if not status:
            msg_dict[cfg.archive_log_dir] = msg

    else:
        # Directory where active log files to be searched are
        status, msg = gen_libs.chk_crt_dir(
            cfg.log_dir, read=True, no_print=True)

        if not status:
            msg_dict[cfg.log_dir] = msg

    # Temporary file where check_log will write to
    basepath = gen_libs.get_base_dir(cfg.outfile)
    status, msg = gen_libs.chk_crt_dir(
        basepath, write=True, create=True, no_print=True)

    if not status:
        msg_dict[basepath] = msg

    # Directory path to where error and failed files are saved to
    status, msg = gen_libs.chk_crt_dir(
        cfg.error_dir, write=True, create=True, no_print=True)

    if not status:
        msg_dict[cfg.error_dir] = msg

    # Directory where files with previous processed files are stored at
    basepath2 = gen_libs.get_base_dir(cfg.processed_file)
    status, msg = gen_libs.chk_crt_dir(
        basepath2, write=True, create=True, no_print=True)

    if not status:
        msg_dict[basepath2] = msg

    return msg_dict


def mvalidate_dirs(cfg):

    """Function:  mvalidate_dirs

    Description:  Validate the directories in the configuration file for the
        -I option.

    Arguments:
        (input) cfg -> Configuration setup
        (output) msg_dict -> Dictionary of any error messages detected

    """

    msg_dict = dict()

    status, msg = gen_libs.chk_crt_dir(
        cfg.monitor_dir, write=True, no_print=True)

    if not status:
        msg_dict[cfg.monitor_dir] = msg

    status, msg = gen_libs.chk_crt_dir(
        cfg.merror_dir, write=True, create=True, no_print=True)

    if not status:
        msg_dict[cfg.merror_dir] = msg

    status, msg = gen_libs.chk_crt_dir(
        cfg.marchive_dir, write=True, create=True, no_print=True)

    if not status:
        msg_dict[cfg.marchive_dir] = msg

    return msg_dict


def checks_dirs(args, cfg):

    """Function:  checks_dirs

    Description:  Validate the directories in the configuration file depending
        on the options selected.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (output) msg_dict -> Dictionary of any error messages detected

    """

    msg_dict = dict()

    if args.get_val("-P", def_val=None):
        msg_dict = validate_dirs(cfg, args)

    elif args.get_val("-I", def_val=None):
        msg_dict = mvalidate_dirs(cfg)

    return msg_dict


def config_override(args, cfg):

    """Function:  config_override

    Description:  Checks for specific arguments which will override the
        values for some configuration settings.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (output) cfg -> Modified configuration setup

    """

    if args.get_val("-n", def_val=None):
        cfg.monitor_dir = args.get_val("-n")

    return cfg


def run_program(args, func_dict):

    """Function:  run_program

    Description:  Controls the running of the program by loading and
        validating the configuration file and calling the function to
        process the docid files.

    Arguments:
        (input) args -> ArgParser class instance
        (input) func_dict -> Dict of function calls for different options

    """

    func_dict = dict(func_dict)
    cfg = gen_libs.load_module(args.get_val("-c"), args.get_val("-d"))
    basepath = gen_libs.get_base_dir(cfg.log_file)
    status, err_msg = gen_libs.chk_crt_dir(
        basepath, write=True, create=True, no_print=True)
    log_file = cfg.log_file + "." + datetime.datetime.strftime(
        datetime.datetime.now(), "%Y%m%d")

    if status:
        log = gen_class.Logger(
            log_file, log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")
        log.log_info("Program initialization.")
        cfg = config_override(args, cfg)
        msg_dict = checks_dirs(args, cfg)

        if msg_dict:
            log.log_err("Validation of configuration directories failed")
            log.log_err("Message: %s" % (msg_dict))

        else:
            for opt in set(args.get_args_keys()) & set(func_dict.keys()):
                func_dict[opt](args, cfg, log)

    else:
        print("Error:  Logger Directory Check Failure")
        print("Error Message: %s" % (err_msg))


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains directories and their octal permissions
        func_dict -> dictionary of function calls for different options
        opt_con_req_dict -> contains options requiring other options
        opt_multi_list -> contains the options that will have multiple values
        opt_req_list -> contains options that are required for the program
        opt_val_list -> contains options which require values
        opt_xor_dict -> contains dict with key that is xor with it's values

    Arguments:
        (input) argv -> Arguments from the command line

    """

    cmdline = gen_libs.get_inst(sys)
    dir_perms_chk = {"-d": 5, "-m": 5, "-n": 7}
    file_perms_chk = {"-F": 4}
    func_dict = {"-P": process_files, "-I": insert_data, "-F": file_input}
    opt_con_req_dict = {"-s": ["-t"]}
    opt_multi_list = ["-s", "-t"]
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d", "-m", "-n", "-s", "-t", "-y"]
    opt_xor_dict = {"-I": ["-P", "-F"], "-P": ["-I", "-F"], "-F": ["-I", "-P"]}

    # Process argument list from command line.
    args = gen_class.ArgParser(
        cmdline.argv, opt_val=opt_val_list, multi_val=opt_multi_list,
        do_parse=True)

    if not gen_libs.help_func(args.get_args(), __version__, help_message)   \
       and args.arg_require(opt_req=opt_req_list)                           \
       and args.arg_cond_req_or(opt_con_or=opt_con_req_dict)                \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk)                    \
       and args.arg_xor_dict(opt_xor_val=opt_xor_dict)                      \
       and args.arg_file_chk(file_perm_chk=file_perms_chk):

        try:
            prog_lock = gen_class.ProgramLock(
                cmdline.argv, args.get_val("-y", def_val=""))
            run_program(args, func_dict)
            del prog_lock

        except gen_class.SingleInstanceException:
            print("WARNING:  Lock in place for pulled_search with id of: %s"
                  % (args.get_val("-y", def_val="")))


if __name__ == "__main__":
    sys.exit(main())
