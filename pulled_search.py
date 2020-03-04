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

# Third-party

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
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


def run_program(args_array, **kwargs):

    """Function:  run_program

    Description:  Controls the running of the program by...

    Arguments:
        (input) args_array -> Dictionary of command line options and values.

    """

    mail = None
    file_remove = list()
    args_array = dict(args_array)

    cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])

    if args_array.get("-t", None):
        mail = gen_class.setup_mail(args_array.get("-t"),
                                    subj=args_array.get("-s", None))

    # Detect new files.
    new_files = gen_libs.list_files(args_array["-m"])

    # Loop on files detected:
    for fname in new_files:

        # Read file.
        file_docid = read_file(fname)

        # Parse from file docid, command, and postdate.
        docid = file_docid["docid"]
        command = file_docid["command"]
        postdate = file_docid["postdate"]

        # Create list of files to check.
        log_list = get_logs(cfg)

        # Create search dictionary to pass to check_log.
        search_args = {"-g": "w", "-f": log_list, "-S": [docid], "-k": "or",
                       "-o": cfg.outfile, "-z": True}

        # Call check_log passing search dictionary to program.
        check_log.run_program(search_args)

        # Open return file from check_log and read in any data.
        if gen_libs.is_empty_file(cfg.outfile):
            file_log = []

        else:
            file_log = read_file(cfg.outfile)

        # Remove cfg.outfile.
        remove_file(cfg.outfile)

        # If data is present then
        if file_log:

            # Convert data to list
                # Might already be a list.

            # Create JSON document containing log entries, docid, servername,
            #   enclave, postdate, command, and currentdate.
            log_json = create_json(docid, postdate, command,
                                   socket.gethostname(), cfg.enclave,
                                   current_dtg) # Get current_dtg

            # Send JSON to RabbitMQ for further processing.
            send_rabbitmq(cfg, log_json)

            # Create file list from processed file.
            file_remove.append(fname)

    # Remove those files in file list.
    for fname in file_remove:
        gen_libs.rm_file(fname)
        new_files.pop(fname)

    # Any files not processed - move to error directory and send email.
    if new_files:
        non_processed_files(new_files, mail, cfg.error_dir)


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
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):
       and arg_parser.arg_cond_req_or(args_array, opt_con_req_dict):

        try:
            prog_lock = gen_class.ProgramLock(sys.argv,
                                              args_array.get("-y", ""))
            run_program(args_array)
            del prog_lock

        except gen_class.SingleInstanceException:
            print("WARNING:  lock in place for pulled_search with id of: %s"
                  % (args_array.get("-y", "")))


if __name__ == "__main__":
    sys.exit(main())
