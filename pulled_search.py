#!/usr/bin/python
# Classification (U)

"""Program:  pulled_search.py

    Description:  The pulled_search program monitors for new files that contain
        docids.  Once detected will search the Apache log files for any entries
        and if detected will send these log entries to a RabbitMQ queue.

    Usage:
        pulled_search.py -c file -d path [-m path | -z | -y flavor_id ]
            [-t email {email2 email3 ...} {-s subject_line}] [-v | -h]

    Arguments:
        -c file => Configuration file.  Required argument.
        -d dir_path => Directory path for option '-c'.  Required argument.
        -m dir_path => Directory to monitor.
        -z => Use the zgrep option instead of check_log to check GZipped files.
        -t email_address(es) => Send output to one or more email addresses.
        -s subject_line => Subject line of email.  Requires -t option.
        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.
        NOTE 2:  -s requires -t option to be included.

        NOTE 3:  The log files can be normal flat files or compressed files
            (e.g. ending with .gz) or a combination there of.  Any other type
            of compressed file will not work.

    Examples:
        pulled_search.py -c search -d config

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

# Third-party
import json

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import rabbit_lib.rabbitmq_class as rabbitmq_class
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


def non_processed(docid_files, error_dir, mail=None, **kwargs):

    """Function:  non_processed

    Description:  Process non-processed files.

    Arguments:
        (input) docid_files -> List of files not processed.
        (input) error_dir -> Error directory for storing non-processed files.
        (input) mail -> Mail instance.

    """

    docid_files = list(docid_files)
    
    for fname in docid_files:
        gen_libs.mv_file2(fname, error_dir)
    
    if docid_files and mail:
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
            # Published good.
            status = True

        else:
            # Published bad.
            status = False

    else:
        # Failed to connect.
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
    dtg = datetime.datetime.strfname(datetime.datetime.now(), "%Y%m%d %H%M%S")
    log_json = {"docID": docid_dict["docid"],
                "command": docid_dict["command"],
                "postDate": docid_dict["postdate"],
                "securityEnclave": cfg.enclave,
                "asOf": dtg,
                "serverName": socket.gethostname(),
                "logEntries": file_log}

    return log_json


def process_docid(cfg, fname, log, **kwargs):

    """Function:  process_docid

    Description:  Processes the docid.

    Arguments:
        (input) cfg -> Configuration setup.
        (input) fname -> Docid file name.
        (input) log -> Log class instance.
        (output) status -> True|False - File has successfully processed.

    """

    file_log = []

    # Read and parse the file.
    data_list = gen_libs.file_2_list(fname)
    docid_dict = json.loads(gen_libs.list_2_str(data_list))

    # Create list of files to check.
    cmd_regex = docid_dict["command"] + "*" + cfg.log_type + "*"
    log_files = gen_libs.dir_file_match(cfg.log_dir, cmd_regex)

    # Create search dictionary to pass to check_log.
    search_args = {"-g": "w", "-f": log_files, "-S": [docid_dict["docid"]],
                   "-k": "or", "-o": cfg.outfile, "-z": True}

    # Call check_log passing search dictionary to program.
    check_log.run_program(search_args)

    # Open return file from check_log and read in any data.
    if not gen_libs.is_empty_file(cfg.outfile):
        log.log_info("process_docid:  Log entries detected.")
        file_log = gen_libs.file_2_list(cfg.outfile)

    # Remove cfg.outfile.
    #   Do I want to do anything with err_flag and err_msg?
    err_flag, err_msg = gen_libs.rm_file(cfg.outfile)

    # If data is present then
    if file_log:
        # Create JSON document.
        log_json = create_json(cfg, docid_dict, file_log)

        # Send JSON to RabbitMQ.
        log.log_info("process_docid:  Log entries publishing to RabbitMQ.")
        status = send_2_rabbitmq(cfg, log_json)
    
    else:
        status = True

    return status


def process_files(args_array, cfg, log, **kwargs):

    """Function:  process_files

    Description:  Processes the docid files.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) cfg -> Configuration setup.
        (input) log -> Log class instance.

    """

    remove_list = list()
    mail = None
    args_array = dict(args_array)

    if args_array.get("-t", None):
        mail = gen_class.setup_mail(args_array.get("-t"),
                                    subj=args_array.get("-s", None))

    # Detect new docid files.
    docid_files = gen_libs.dir_file_match(cfg.docid_dir, cfg.file_regex)

    # Loop on files detected.
    for fname in docid_files:
        log.log_info("process_files:  Processing file: %s" %(fname))
        status = process_docid(cfg, fname, log)

        if status:
            # Create file list from processed file.
            remove_list.append(fname)

    # Remove those files in file list.
    for fname in remove_list:
        gen_libs.rm_file(fname)
        docid_files.pop(fname)

    # Any files not processed - move to error directory and send email.
    if docid_files:
        log.log_info("process_files:  Non-processed files detected.")
        non_processed(docid_files, cfg.error_dir, mail)


def validate_dirs(cfg, **kwargs):

    """Function:  validate_dirs

    Description:  Validate the directories in the configuration file.

    Arguments:
        (input) cfg -> Configuration setup.
        (output) msg_dict -> Dictionary of any error messages detected.

    """

    msg_dict = dict()

    # Check for directory existence in cfg configuration.
    status, err_msg = gen_libs.chk_crt_file(cfg.doc_dir, write=True,
                                            no_print=True)

    if not status:
        msg_dict[cfg.doc_dir] = msg

    status, err_msg = gen_libs.chk_crt_file(cfg.log_dir, read=True,
                                            no_print=True)

    if not status:
        msg_dict[cfg.log_dir] = msg

    basepath = gen_libs.get_base_dir(cfg.outfile)
    status, err_msg = gen_libs.chk_crt_file(basepath, write=True,
                                            create=True, no_print=True)

    if not status:
        msg_dict[basepath] = msg

    status, err_msg = gen_libs.chk_crt_file(cfg.error_dir, write=True,
                                            create=True, no_print=True)

    if not status:
        msg_dict[cfg.error_dir] = msg

    return msg_dict


def run_program(args_array, **kwargs):

    """Function:  run_program

    Description:  Controls the running of the program by loading and
        validating the configuration file and calling the function to
        process the docid files.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.

    """

    args_array = dict(args_array)
    cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])
    status, err_msg = gen_libs.chk_crt_file(cfg.log_file, write=True,
                                            create=True, no_print=True)

    if status:
        log = gen_class.Logger(cfg.log_file, cfg.log_file, "INFO",
                               "%(asctime)s %(levelname)s %(message)s",
                               "%Y-%m-%dT%H:%M:%SZ")
        log.log_info("Program initialization...")

        if args_array.get("-m", None):
            cfg.docid_dir = args_array["-m"]

        msg_dict = validate_dirs(cfg)

        if msg_dict:
            log.log_err("Validation of configuration directories failed")
            log.log_err("Message: %s" % (msg_dict))
            mail = gen_class.setup_mail(cfg.admin_email,
                                        subj="Directory Check Failure")
            mail.add_2_msg(msg_dict)
            mail.send_mail()

        else:
            log.log_info("Detecting files...")
            process_files(args_array, cfg, log)

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
        opt_con_req_dict -> contains options requiring other options.
        opt_multi_list -> contains the options that will have multiple values.
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    dir_chk_list = ["-d", "-m"]
    opt_con_req_dict = {"-s": ["-t"]}
    opt_multi_list = ["-s", "-t"]
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d", "-m", "-s", "-t", "-y"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list,
                                       multi_val=opt_multi_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list) \
       and arg_parser.arg_cond_req_or(args_array, opt_con_req_dict):

        try:
            prog_lock = gen_class.ProgramLock(sys.argv,
                                              args_array.get("-y", ""))
            run_program(args_array)
            del prog_lock

        except gen_class.SingleInstanceException:
            print("WARNING:  Lock in place for pulled_search with id of: %s"
                  % (args_array.get("-y", "")))


if __name__ == "__main__":
    sys.exit(main())
