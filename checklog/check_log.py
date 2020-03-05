#!/usr/bin/python
# Classification (U)

"""Program:  check_log.py

    Description:  The check_log program checks log files or "standard in" for
        new data since the last run as determined by the contents of the marker
        file.  The program can also setup filtering options to either ignore
        specific messages, search for specific formatted messages, and/or
        do multiple keyword searching using the and | or predicate search.
        See -F, -S, and -i options below for further details.

    Usage:
        check_log.py [-f {file* file1 file2 ...}] [-F file | -i file
            | -m file | -o file | -n | -r | -c | -y flavor_id | -z
            | -S {keyword1 keyword2 ...} | -g {a|w} | -w]
            [-t email {email2 email3 ...} {-s subject_line}] [-v | -h]

        standard in | check_log.py ...

    Arguments:
        -f file(s) => Name(s) of the log files to check.  Can also use
            wildcard expansion for file names.  Can include both normal
            flat files or .gz compressed files.
        -F file => Name of file that contains regex format expression.  The
            file will contain one or more regex expressions to be used to
            filter out data that does not match the regex string.  If
            multiple regex expressions are present will use "or" logic.
            See NOTES below for formatting of regex expressions.
        -t email_address(es) => Send output to one or more email addresses.
        -s subject_line => Subject line of email.  Requires -t option.
        -i file => Name of the file that contains entries to be ignored.  The
            entries are case-insensitive.
        -m file => Name of the file that contains marker tag in file.
        -o file => Name of the out file.
        -n => Flag option not to update the marker file.
        -r => Flag option to recheck the entire log file.
        -c => Flag option to clear the contents in the marker file.  Requires
            -m option.
        -S keyword(s) => Search for keywords.  List of keywords are
            space-delimited and are case-insensitive.
        -k "and"|"or" => Keyword search logic.  Default is "or".
        -g "a"|"w" => Append or write (overwrite) to a log file.  Default is w.
        -w => No write if empty.  Do not write to a file if no data was found.
        -y value => A flavor id for the program lock.  To create unique lock.
        -z => Suppress standard out.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.
        NOTE 2:  -c requires -m option to be included.
        NOTE 3:  -s requires -t option to be included.

        NOTE 4:  Regex expression formatting: Uses standard regex formatting.
            The regex expression can contain multiple expressions, but will use
            "or" logic to determine whether a data string is allowed through.
            Use the "|" as the delimitered between expressions or place each
            regex expression on a line by itself in the file.

            Example of checking for a format such as this:
                2017-04-04T11:24:32.345+0000

            Regex format string:
                \d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+0000

            Example of checking for a date or time format such as:
                2017-04-04
                22:24:32
            Regex format strings:
                \d{4}\-\d{2}\-\d{2}|d{2}:\d{2}:\d{2}

        NOTE 5:  The log files can be normal flat files or compressed files
            (e.g. ending with .gz) or a combination there of.  Any other type
            of compressed file will not work.

    Examples:
        File input example:
            check_log.py -f /opt/sybase/errorlog* -o /tmp/out_file -n

        Standard in example:
            cat errorlog | check_log.py -o /tmp/out_file -S Error Warn

"""

# Libraries and Global Variables

# Standard
# For Python 2.6/2.7: Redirection of stdout in a print command.
from __future__ import print_function
import sys
import os
import re
import socket
import getpass

# Third-party

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def full_chk(args_array, **kwargs):

    """Function:  full_chk

    Description:  Sets the full check flag depending on options selected.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (output) True|False -> Determine full check of log.

    """

    args_array = dict(args_array)
    full_chk_flag = True

    if "-m" in args_array and "-r" not in args_array \
       and not gen_libs.is_empty_file(args_array["-m"]):

        full_chk_flag = False

    return full_chk_flag


def find_marker(log, **kwargs):

    """Function:  find_marker

    Description:  Locates the marker.

    Arguments:
        (input) log -> LogFile class instance.

    """

    if log.marker:
        log.find_marker(update=True)


def update_marker(args_array, line, **kwargs):

    """Function:  update_marker

    Description:  Writes the last line of the log to the marker file, if the
        marker option is selected and not the no_update option.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) line -> Last line of log.

    """

    args_array = dict(args_array)

    if "-m" in args_array and "-n" not in args_array:
        gen_libs.write_file(args_array["-m"], mode="w", data=line)


def log_2_output(log, args_array, **kwargs):

    """Function:  log_2_output

    Description:  Sends the log array to output depending on command line
        option.

    Arguments:
        (input) log -> LogFile class instance.
        (input) args_array -> Dictionary of command line options and values.

    """

    args_array = dict(args_array)

    # Send output to email.
    if "-t" in args_array:
        host = socket.gethostname()
        frm_line = getpass.getuser() + "@" + host

        mail = gen_class.Mail(args_array["-t"],
                              "".join(args_array.get("-s",
                                                     "check_log: " + host)),
                              frm_line)
        mail.add_2_msg("\n".join(log.loglist))
        mail.send_mail()

    # Write output to file.
    if "-o" in args_array and (log.loglist or "-w" not in args_array):
        with open(args_array["-o"], args_array["-g"]) as f_hdlr:
            for x in log.loglist:
                print(x, file=f_hdlr)

    # Suppress standard out.
    if "-z" not in args_array:
        for x in log.loglist:
            print(x, file=sys.stdout)


def fetch_log(log, args_array, **kwargs):

    """Function:  fetch_log

    Description:  Sorts the log files from oldest to newest, finds the place to
        start pulling the log entries; either at the marker or the
        oldest log file.  Appends the log entries to an array which is
        passed to the calling function.

    Arguments:
        (input) log -> LogFile class instance.
        (input) args_array -> Dictionary of command line options and values.

    """

    args_array = dict(args_array)

    # Sort files from oldest to newest.
    args_array["-f"] = sorted(args_array["-f"], key=os.path.getmtime,
                              reverse=False)

    log_file = gen_libs.openfile(args_array["-f"][0], "r")

    # Start with the log file returned by open_log function call.
    for x in args_array["-f"][args_array["-f"].index(log_file.name):]:

        # If file is closed, open up next one.
        if log_file.closed:
            log_file = gen_libs.openfile(x, "r")

        log.load_loglist(log_file)
        log_file.close()


def fetch_log_stdin(log, **kwargs):

    """Function:  fetch_log_stdin

    Description:  Reads 'standard in' into an array, finds the place to start
        pulling the log entries; either at the marker or at the start of
        the array.

    Arguments:
        (input) log -> LogFile class instance.
        (input) args_array -> Dictionary of command line options and values.

    """

    for ln in sys.stdin:
        log.load_loglist(str(ln))


def load_attributes(log, args_array, **kwargs):

    """Function:  load_attributes

    Description:  Checks for certain program options to be loaded into the
        LogFile class attributes.

    Arguments:
        (input) log -> LogFile class instance.
        (input) args_array -> Dictionary of command line options and values.

    """

    if "-S" in args_array.keys():
        log.load_keyword(args_array["-S"])

    if "-k" in args_array.keys():
        log.set_predicate(args_array["-k"])

    if "-m" in args_array.keys():
        log.load_marker(gen_libs.openfile(args_array["-m"]))

    if "-F" in args_array.keys():
        log.load_regex(gen_libs.openfile(args_array["-F"]))

    if "-i" in args_array.keys():
        log.load_ignore(gen_libs.openfile(args_array["-i"]))


def run_program(args_array, **kwargs):

    """Function:  run_program

    Description:  Controls the running of the program by fetching the log
        entries, updating the file marker, and sending the log entries to
        output.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.

    """

    args_array = dict(args_array)

    if "-c" in args_array and "-m" in args_array:
        gen_libs.clear_file(args_array["-m"])

    else:
        log = gen_class.LogFile()
        load_attributes(log, args_array)

        if "-f" in args_array:
            fetch_log(log, args_array)

        elif not sys.stdin.isatty():
            fetch_log_stdin(log)

        if log.loglist:
            if not full_chk(args_array):
                find_marker(log)

            log.filter_keyword()
            log.filter_ignore()
            log.filter_regex()
            log_2_output(log, args_array)
            update_marker(args_array, log.lastline)


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        file_chk_list -> contains the options which will have files included.
        file_crt_list -> contains options which require files to be created.
        opt_con_req_dict -> contains options requiring other options.
        opt_multi_list -> contains the options that will have multiple values.
        opt_val_list -> contains options which require values.
        opt_valid_val -> contains options with their valid values.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    file_chk_list = ["-f", "-i", "-m", "-F"]
    file_crt_list = ["-m"]
    opt_con_req_dict = {"-c": ["-m"], "-s": ["-t"]}
    opt_multi_list = ["-f", "-s", "-t", "-S"]
    opt_val_list = ["-i", "-m", "-o", "-s", "-t", "-y", "-F", "-S", "-k", "-g"]
    opt_valid_val = {"-k": ["and", "or"], "-g": ["a", "w"]}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list,
                                       multi_val=opt_multi_list)

    # Set default search logic.
    if "-S" in args_array.keys() and "-k" not in args_array.keys():
        args_array["-k"] = "or"

    # Set default write file mode.
    if "-g" not in args_array.keys():
        args_array["-g"] = "w"

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and arg_parser.arg_cond_req_or(args_array, opt_con_req_dict) \
       and not arg_parser.arg_file_chk(args_array, file_chk_list,
                                       file_crt_list) \
       and arg_parser.arg_valid_val(args_array, opt_valid_val):

        try:
            prog_lock = gen_class.ProgramLock(sys.argv,
                                              args_array.get("-y", ""))
            run_program(args_array)
            del prog_lock

        except gen_class.SingleInstanceException:
            print("WARNING:  lock in place for check_log with id of: %s"
                  % (args_array.get("-y", "")))


if __name__ == "__main__":
    sys.exit(main())
