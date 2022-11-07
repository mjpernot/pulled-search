#!/usr/bin/python
# Classification (U)

"""Program:  pulled_search.py

    Description:  The pulled_search program is a multi-optional program for use
        with the pulled product process.  It can detect when new pulled product
        files are created, parse the file, call the search program to check log
        files for the docid in the file.  Any entries found will be converted
        into a JSON document and send to a RabbitMQ queue.  The program also
        has the ability to detect when new search pulled product log entries
        are available to be inserted into a database.

    Usage:
        pulled_search.py -c file -d path
            {-P [-m path] [-a] [-z] |
             -I [-n path]}
            [-t email {email2 email3 ...} {-s subject_line}]
            [-y flavor_id]
            [-v | -h]

    Arguments:
        -c file => Configuration file.  Required argument.
        -d dir_path => Directory path for option '-c'.  Required argument.

        -P => Process Doc ID files send to RabbitMQ.
            -m dir_path => Directory to monitor for doc ID files.
            -a => This is an archive log search.
            -z => Use the zgrep option instead of check_log to check GZipped
                files.

        -I => Insert Pulled Search files into Mongodb.
            -n dir_path => Directory to monitor for pulled search files.

        -t email_address(es) => Send output to one or more email addresses.
            -s subject_line => Pre-amble to the subject line of email.

        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.
        NOTE 2:  -s requires -t option to be included.
        NOTE 3:  -P and -I are XOR options.
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
            # This section is for either the -P or -I option.
            # Logger file for the storage of log entries.
            # File name including directory path.
            log_file = "BASE_PATH/log/pulled_search.log"

            # Pulled Search Process Configuration section.
            # Update this section if using the -P option.
            # Directory where docid files to be processed are.
            doc_dir = ["DOC_DIR_PATH", "DOC_DIR_PATH2"]
            # Directory where files with previous processed files are stored at
            processed_dir = "BASE_PATH/processed"
            # File name for previous processed files.
            processed_file = "processed"
            # Regular expression for search for log file names.
            file_regex = "-PULLED-"

            # Directory where active log files to be searched are.
            log_dir = "LOG_DIR_PATH"
            # Type of log files to checked.
            log_type = "access_log"
            # Directory where archived log files to be searched are.
            archive_log_dir = "ARCHIVE_DIR_PATH"
            # Temporary file where check_log will write to.
            # File name including directory path.
            outfile = "BASE_PATH/tmp/checklog.out"
            # Security enclave these files are being processed on.
            enclave = "ENCLAVE"
            # Directory path to where error and non-processed files are saved.
            error_dir = "BASE_PATH/search_error"
            # Mapping of commands to keywords.
            # This is for the naming of the access logs which are not always
            #   under the command name.
            command = {"intelink": "eucom"}

            # Pulled Search Process/RabbitMQ Configuration section.
            # Update this section if using the -P option.
            # Fill either the mail section to send to RabbitMQ via email or
            #   fill in the RabbitMQ section to publish to RabbitMQ directly.
            #   If using mail option this is normally used in conjunction with
            #   the rmq_2_mail.py program.
            # Note: If the email is filled in then this will override the
            #   RabbitMQ section.
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
            # Example: host_list =
            #   ["hostname:5672", "hostname2:5672", "hostname:5673"]
            # Note:  If host_list is set, it will take precedence over the host
            #   entry.
            host_list = []
            # RabbitMQ Queue name.
            queue = "QUEUENAME"
            # RabbitMQ Routing Key
            r_key = "ROUTING_KEY"
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
            # Update this section if using the -I option.
            # Directory where to monitor for new files to insert into Mongodb.
            monitor_dir = "MONITOR_DIR_PATH"
            # Regular expression for search for Insert/Mongodb file names.
            mfile_regex = "_mongo.json"
            # Directory path to where Insert/Mongodb archived files are saved
            #   to.
            marchive_dir = "BASE_PATH/archive"
            # Directory path to where Insert/Mongodb error and non-processed
            #   files are saved to.
            merror_dir = "BASE_PATH/mongo_error"
            # Name of Mongo configuration file.  (Do not include the ".py"
            #   in the name.)
            # No not change unless changing the name of the external Mongo
            #   config file.
            mconfig = "mongo"

        Mongo configuration file format (config/mongo.py.TEMPLATE).  The
            configuration file format is for connecting to a Mongo database or
            replica set for monitoring.  A second configuration file can also
            be used to connect to a Mongo database or replica set to insert the
            results of the performance monitoring into.

            There are two ways to connect methods:  single Mongo database or a
            Mongo replica set.

            Single database connection:

            # Single Configuration file for Mongo Database Server.
            user = "USER"
            japd = "PSWORD"
            host = "HOST_IP"
            name = "HOSTNAME"
            port = 27017
            conf_file = None
            auth = True
            auth_db = "admin"
            auth_mech = "SCRAM-SHA-1"

            Replica set connection:  Same format as above, but with these
                additional entries at the end of the configuration file.  By
                default all these entries are set to None to represent not
                connecting to a replica set.

            repset = "REPLICA_SET_NAME"
            repset_hosts = "HOST1:PORT, HOST2:PORT, HOST3:PORT, [...]"
            db_auth = "AUTHENTICATION_DATABASE"

            Note:  If using SSL connections then set one or more of the
                following entries.  This will automatically enable SSL
                connections. Below are the configuration settings for SSL
                connections.  See configuration file for details on each entry:

            ssl_client_ca = None
            ssl_client_key = None
            ssl_client_cert = None
            ssl_client_phrase = None

            Note:  FIPS Environment for Mongo.
              If operating in a FIPS 104-2 environment, this package will
              require at least a minimum of pymongo==3.8.0 or better.  It will
              also require a manual change to the auth.py module in the pymongo
              package.  See below for changes to auth.py.

            - Locate the auth.py file python installed packages on the system
                in the pymongo package directory.
            - Edit the file and locate the "_password_digest" function.
            - In the "_password_digest" function there is an line that should
                match: "md5hash = hashlib.md5()".  Change it to
                "md5hash = hashlib.md5(usedforsecurity=False)".
            - Lastly, it will require the Mongo configuration file entry
                auth_mech to be set to: SCRAM-SHA-1 or SCRAM-SHA-256.

            # Name of Mongo database for data insertion
            db = "DATABASE"
            # Name of Mongo table/collection.
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
import subprocess

# Third-party
import json
import platform
import decimal
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


def create_json(cfg, docid_dict, file_log):

    """Function:  create_json

    Description:  Create the JSON from the docid file and log entries.

    Arguments:
        (input) cfg -> Configuration setup
        (input) docid_dict -> Dictionary of docid file
        (input) file_log -> List of log file entries
        (output) log_json -> Dictionary of docid file and log entries

    """

    docid_dict = dict(docid_dict)
    file_log = list(file_log)
    dtg = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d %H%M%S")
    log_json = {"DocID": docid_dict["docid"],
                "Command": docid_dict["command"],
                "PubDate": docid_dict["pubdate"],
                "SecurityEnclave": cfg.enclave,
                "AsOf": dtg,
                "ServerName": socket.gethostname(),
                "LogEntries": file_log}

    return log_json


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


def zgrep_search(file_list, keyword, outfile):

    """Function:  zgrep_search

    Description:  Zgrep compressed files for keyword and write to file.

    NOTE:  This is for use on Centos 2.6.X systems and earlier.

    Arguments:
        (input) file_list -> List of files to search
        (input) keyword -> Value to search for
        (input) outfile -> File to write the results to

    """

    subp = gen_libs.get_inst(subprocess)
    file_list = list(file_list)
    cmd = "zgrep"

    for fname in file_list:

        # Search for keyword and write to file.
        with open(outfile, "ab") as fout:
            proc1 = subp.Popen([cmd, keyword, fname], stdout=fout)
            proc1.wait()


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
    cmd = docid_dict["command"].lower()

    # Check to see if the command is mapped to a different keyword file
    if cmd in cfg.command:
        cmd = cfg.command[cmd]

    cmd_regex = cmd + ".*" + cfg.log_type

    if args.get_val("-a", def_val=None):
        log.log_info("process_docid:  Searching for archive log files...")
        log_files = get_archive_files(
            cfg.archive_log_dir, cmd, docid_dict["pubdate"], cmd_regex)

    else:
        log.log_info("process_docid:  Searching for apache log files...")
        log_files = gen_libs.filename_search(cfg.log_dir, cmd_regex,
                                             add_path=True)

    # Determine if running on a pre-7 CentOS system.
    is_centos = \
        True if "centos" in platform.linux_distribution()[0].lower() else False
    is_pre_7 = \
        decimal.Decimal(platform.linux_distribution()[1]) < \
        decimal.Decimal('7.0')

    # Must use zgrep searching in pre-7 Centos systems.
    if args.get_val("-z", def_val=False) or (is_centos and is_pre_7):
        log.log_info("process_docid:  Running zgrep search...")
        zgrep_search(log_files, docid_dict["docid"], cfg.outfile)

    else:
        # Create argument list for check_log program.
        cmdline = [
            "check_log.py", "-g", "w", "-f", log_files, "-S",
            [docid_dict["docid"]], "-k", "or", "-o", cfg.outfile, "-z"]
        chk_opt_val = ["-g", "-f", "-S", "-k", "-o"]
        chk_args = gen_class.ArgParser(
            cmdline, opt_val=chk_opt_val, do_parse=True)
        log.log_info("process_docid:  Running check_log search...")
        check_log.run_program(chk_args)

    if not gen_libs.is_empty_file(cfg.outfile):
        log.log_info("process_docid:  Log entries detected.")
        file_log = gen_libs.file_2_list(cfg.outfile)
        log_json = create_json(cfg, docid_dict, file_log)
        process_json(args, cfg, log, log_json)

    else:
        log.log_info("process_docid:  No log entries detected.")

    err_flag, err_msg = gen_libs.rm_file(cfg.outfile)

    if err_flag:
        log.log_warn("process_docid:  %s" % (err_msg))

    return status


def process_json(args, cfg, log, log_json):

    """Function:  process_json

    Description:  Process the JSON document from the pulled search results.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance
        (input) log_json -> JSON log document

    """

    if cfg.to_addr and cfg.subj:
        log.log_info("process_json:  Emailing log entries...")
        mail = gen_class.setup_mail(cfg.to_addr, subj=cfg.subj)
        mail.add_2_msg(log_json)
        mail.send_mail()

    else:
        log.log_info("process_json:  Publishing log entries...")
        status, err_msg = rabbitmq_class.pub_2_rmq(
            cfg, json.dumps(log_json))

        if status:
            log.log_info(
                "process_json:  Log entries published to RabbitMQ.")

        else:
            log.log_err(
                "process_json:  Error detected during publication.")
            log.log_err("process_json:  Message: %s" % (err_msg))
            dtg = datetime.datetime.strftime(
                datetime.datetime.now(), "%Y%m%d_%H%M%S")
            name = "NonPublished." + log_json["DocID"] \
                + log_json["ServerName"] + "." + dtg
            fname = os.path.join(cfg.error_dir, name)
            gen_libs.write_file(fname, mode="w", data=log_json)
            subj = args.get_val("-s", def_val="") + "Error: NonPublished"

            if args.get_val("-t", def_val=False):
                mail = gen_class.setup_mail(args.get_val("-t"), subj=subj)
                mail.add_2_msg("Unable to publish message to RabbitMQ")
                mail.add_2_msg("File: " + fname)
                mail.send_mail()


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
    data_list = gen_libs.file_2_list(fname)
    insert_dict = json.loads(gen_libs.list_2_str(data_list))

    if isinstance(insert_dict, dict):
        log.log_info("process_insert:  Inserting data into Mongodb.")
        mcfg = gen_libs.load_module(cfg.mconfig, args.get_val("-d"))
        mongo_stat = mongo_libs.ins_doc(mcfg, mcfg.dbs, mcfg.tbl, insert_dict)

        if not mongo_stat[0]:
            log.log_err("process_insert:  Insert of data into MongoDB failed.")
            log.log_err("Mongo error message:  %s" % (mongo_stat[1]))
            status = False

        else:
            log.log_info("process_insert:  Mongo database insertion.")
            status = True

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

    Description:  Read in the previous processed file names.

    Arguments:
        (input) processed_fname -> Name of processed file
        (output) processed_files -> List of processed file names

    """

    # Part of number 3 will be it's own function.
    # load_processed(processed_fname)
    #   Out: processed_files
    # 3. Load processed file into list.
    # Load the previous processed docids from file
    try:
        with open(processed_fname) as fhdr:
            processed_files = fhdr.readlines()
            processed_files = [line.rstrip() for line in processed_files]

    except IOError as msg:
        if msg.args[1] == "No such file or directory":
            processed_files = list()

    return processed_files


def update_processed(log, processed_fname, file_dict):

    """Function:  update_processed

    Description:  Update the processed file with new file entries.

    Arguments:
        (input) log -> Log class instance
        (input) processed_fname -> Name of processed file
        (input) file_dict -> Dictionary list of new files processed

    """

    # Part of number 6 will be it's own function.
    # update_processed(log, processed_fname, file_dict)
    # 6. Add file_dict to list of files already processed this month.
    log.log_info("update_processed:  Updating processed file: %s"
                 % (processed_fname))
    file_dict = dict(file_dict)

    with open(processed_fname, "a") as fhdr:
        for item in file_dict:
            fhdr.write(file_dict[item] + "\n")


def process_failed(args, cfg, log, failed_dict):

    """Function:  process_failed

    Description:  Process the failed files.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance
        (input) failed_dict -> Dictionary list of failed files

    """

    # Part of number 7 will be it's own function.
    # process_failed(args, cfg, log, failed_file)
    # 7. Process failed list -> email? Yes, if passed, file? Yes
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

    # recall_search(args, cfg, log, file_dict)
    #   Out: failed_dict
    # 5. Loop on the new file list (file_dict) and regex for security recall.
    # Search for security violation entries
    log.log_info("recall_search:  Processing new pulled files.")
# Should pattern be placed into config file?
#    pattern = "JAC.pull.subtype.*.SECURITY RECALL"
    lines = list()
    err_msg = dict()
    docid_dict = dict()
    failed_dict = dict()
    file_dict = dict(file_dict)

    for fname in file_dict:
        log.log_info("recall_search:  Searching: %s" % (fname))
        try:
            with open(file_dict[fname], "r") as fhdr:
                data = fhdr.readlines()
                lines = [line.rstrip() for line in data]

        except IOError as msg:
            failed_dict[fname] = msg.args[1]
            lines = list()

        log.log_info("recall_search:  Searching for security recall in file.")
        for line in lines:
    #   a. If security recalled then
            if re.search(cfg.pattern, line):
    #       i. Create docid_dict from filename.
                docid_dict["command"] = fname.split("-")[0]
                docid_dict["pubdate"] = fname.split("-")[4]
                docid_dict["docid"] = re.split("-|\.", fname)[7]
                break

    #       ii. Call process_docid (replace fname with docid_dict)
        if docid_dict:
            log.log_info("recall_search:  Processing file: %s" % (fname))
            status = process_docid(args, cfg, docid_dict, log)
            docid_dict = dict()

    #       iii. If not status then add to failed_list
            if not status:
                log.log_err("%s: Failed the process_docid process."
                            % (docid_dict))
                failed_dict[fname] = "Failed the process_docid process"

#        docid_dict = dict() # Not required here, see above.
#        lines = list() # Do not think I need this line.

    # This line being replaced with above code.
    """
    remove_list = process_list(args, cfg, log, docid_files, "search")
    docid_files = cleanup_files(docid_files, done_list, cfg.archive_dir, log)
    """

    return failed_dict


def process_files(args, cfg, log):

    """Function:  process_files

    Description:  Processes the docid files.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance

    """

    # 1. Search for PULLED files from doc_dir directories (may contain dupes).
    # Search for pulled files with doc_dir directories in YYYY/MM
    log.log_info("process_files:  Locating pulled files.")
    docid_files = list()
    yearmon = datetime.date.strftime(datetime.datetime.now(), "%Y/%m")
    yearmon2 = datetime.date.strftime(datetime.datetime.now(), "%Y%m")
    search_dir = list()

    if args.get_val("-m", def_val=None):
        search_dir = [args.get_val("-m")]

    else:
        for dir_entry in cfg.doc_dir:
            search_dir.append(os.path.join(dir_entry, yearmon))

    for docdir in search_dir:
        log.log_info("process_files:  Searching: %s" % (docdir))
        tmp_list = gen_libs.filename_search(
            docdir, cfg.file_regex, add_path=True)
        docid_files.extend(tmp_list)

    # These lines being replaced with above code.
    """
    log.log_info("process_files:  Processing files to search...")
    docid_files = gen_libs.filename_search(
        cfg.doc_dir, cfg.file_regex, add_path=True)
    """

    # 2. Remove dupes from docid_files based on filename (not path).
    # Convert file list to dictionary and remove duplicates
    log.log_info("process_files:  Removing duplicate pulled files.")
    file_dict = {}

    for full_filename in docid_files:
        file_name = os.path.basename(full_filename)

        if file_name not in file_dict:
            file_dict[file_name] = full_filename

    # Part of number 3 will be it's own function.
    # load_processed(processed_fname)
    #   Out: processed_files
    ########################################################################
    # 3. Load processed file into list.
    # Load the previous processed docids from file
    log.log_info("process_files:  Removing previous processed files.")
    processed_fname = os.path.join(
        cfg.processed_dir, cfg.processed_file + "." + yearmon2)
    processed_files = load_processed(processed_fname)

    """
    try:
        with open(processed_fname) as fhdr:
            processed_files = fhdr.readlines()
            processed_files = [line.rstrip() for line in processed_files]

    except IOError as msg:
        if msg[1] == "No such file or directory":
            processed_files = list()
    """
    ########################################################################

    # 4. Remove previous processed files from docid_files (file_dict).
    # Remove previous processed files from file_dict
    for p_filename in processed_files:
        if p_filename in file_dict:
            file_dict.pop(p_filename)

    # Number 5 will be it's own function.
    # recall_search(args, cfg, log, file_dict)
    #   Out: failed_dict
    ########################################################################
    # 5. Loop on the new file list (file_dict) and regex for security recall.
    # Search for security violation entries
    failed_dict = recall_search(args, cfg, log, file_dict)

    """
    log.log_info("process_files:  Processing new files.")
    # Should pattern be placed into config file?
    pattern = "JAC.pull.subtype.*.SECURITY RECALL"
    lines = list()
    err_msg = dict()
    docid_dict = dict()
    failed_dict = dict()

    for fname in file_dict:
        try:
            with open(file_dict[fname]) as fhdr:
                lines = fhdr.readlines()
                lines = [line.rstrip() for line in lines]

        except IOError as msg:
            failed_dict[fname] = msg[1]
            lines = list()

        log.log_info("process_files:  Searching for security recall in file.")
        for line in lines:
    #   a. If security recalled then
            if re.search(pattern, line):
    #       i. Create docid_dict from filename.
                docid_dict["command"] = line.split("-")[0]
                docid_dict["pubdate"] = line.split("-")[4]
                docid_dict["docid"] = re.split("-|\.", line)[7]
                break

    #       ii. Call process_docid (replace fname with docid_dict)
        if docid_dict:
            log.log_info("process_files:  Processing file: %s" % (fname))
            status = process_docid(args, cfg, docid_dict, log)
            docid_dict = dict()

    #       iii. If not status then add to failed_list
            if not status:
                failed_dict[fname] = "Failed the process_docid process"

#        docid_dict = dict() # Not required here, see above.
#        lines = list() # Do not think I need this line.
    """

    # These lines are being replaced with above code.
    """
    remove_list = process_list(args, cfg, log, docid_files, "search")
    docid_files = cleanup_files(docid_files, done_list, cfg.archive_dir, log)
    """
    ########################################################################

    # Part of number 6 will be it's own function.
    # update_processed(log, processed_fname, file_dict)
    ########################################################################
    # 6. Add file_dict to list of files already processed this month.
    if file_dict:
        update_processed(log, processed_fname, file_dict)

        """
        log.log_info("process_files:  Updating previous processed file.")

        with open(processed_fname, "a") as fhdr:
            for item in file_dict:
                fhdr.write(file_dict[item])
        """
    ########################################################################

    # 7. Process failed list -> email? Yes, if passed, file? Yes
    if failed_dict:
        process_failed(args, cfg, log, failed_dict)

    # Part of number 7 will be it's own function.
    # process_failed(args, cfg, log, failed_dict)
    ########################################################################
    """
        log.log_info("process_files:  Processing failed entries.")
        failed_file =

        with open(failed_file, "a") as fhdr:
            # Convert failed_dict to a string.
            fhdr.write(failed_dict)

        # Send email if possible
        if args.get_val("-t", def_val=False):
            subj = args.get_val(
                "-s", def_val="") + "Searched non-processed files"
            mail = gen_class.setup_mail(args.get_val("-t"), subj=subj)
            mail.add_2_msg(failed_dict)
            mail.send_mail()
    """
    ########################################################################

    # This line being replaced with above code.
    """
    non_processed(docid_files, cfg.error_dir, log, mail)
    """


def insert_data(args, cfg, log):

    """Function:  insert_data

    Description:  Insert pulled search files into Mongodb.

    Arguments:
        (input) args -> ArgParser class instance
        (input) cfg -> Configuration setup
        (input) log -> Log class instance

    """

    processed_list = list()
    mail = None

    if args.get_val("-t", def_val=False):
        subj = args.get_val("-s", def_val="") + "Non-processed files"
        mail = gen_class.setup_mail(args.get_val("-t"), subj=subj)

    log.log_info("insert_data:  Processing files to insert...")
    insert_list = gen_libs.filename_search(
        cfg.monitor_dir, cfg.mfile_regex, add_path=True)

    ########################################################################
    for fname in insert_list:
        log.log_info("insert_data:  Processing file: %s" % (fname))
        status = process_insert(args, cfg, fname, log)

        if status:
            processed_list.append(fname)
# This line being replaced with above code.
#    processed_list = process_list(args, cfg, log, insert_list, "insert")
    ########################################################################

    if insert_list:
        nonproc_list = cleanup_files(
            insert_list, processed_list, cfg.marchive_dir, log)
        non_processed(nonproc_list, cfg.merror_dir, log, mail)


def validate_dirs(cfg):

    """Function:  validate_dirs

    Description:  Validate the directories in the configuration file for the
        -P option.

    Arguments:
        (input) cfg -> Configuration setup
        (output) msg_dict -> Dictionary of any error messages detected

    """

    msg_dict = dict()

    # Directory where Docid Pulled Html files are located at
    for entry in cfg.doc_dir:
        status, msg = gen_libs.chk_crt_dir(entry, read=True, no_print=True)

        if not status:
            msg_dict[entry] = msg

    # Directory where log files to be searched are
    status, msg = gen_libs.chk_crt_dir(cfg.log_dir, read=True, no_print=True)

    if not status:
        msg_dict[cfg.log_dir] = msg

    # Directory path to where archived log files to be searched are
    status, msg = gen_libs.chk_crt_dir(
        cfg.archive_log_dir, read=True, no_print=True)

    if not status:
        msg_dict[cfg.archive_log_dir] = msg

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
    status, msg = gen_libs.chk_crt_dir(
        cfg.processed_dir, write=True, create=True, no_print=True)

    if not status:
        msg_dict[cfg.processed_dir] = msg

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
        msg_dict = validate_dirs(cfg)

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

# Moved to process_files
    """
    if args.get_val("-m", def_val=None):
        cfg.doc_dir = [args.get_val("-m")]
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
    func_dict = {"-P": process_files, "-I": insert_data}
    opt_con_req_dict = {"-s": ["-t"]}
    opt_multi_list = ["-s", "-t"]
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d", "-m", "-n", "-s", "-t", "-y"]
    opt_xor_dict = {"-I": ["-P"], "-P": ["-I"]}

    # Process argument list from command line.
    args = gen_class.ArgParser(
        cmdline.argv, opt_val=opt_val_list, multi_val=opt_multi_list,
        do_parse=True)

    if not gen_libs.help_func(args.get_args(), __version__, help_message)   \
       and args.arg_require(opt_req=opt_req_list)                           \
       and args.arg_cond_req_or(opt_con_or=opt_con_req_dict)                \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk)                    \
       and args.arg_xor_dict(opt_xor_val=opt_xor_dict):

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
