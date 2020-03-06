#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in pulled_search.py.

    Usage:
        test/unit/pulled_search/run_program.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import pulled_search
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class MailTest(object):

    """Class:  MailTest

    Description:  Class which is a representation of a Mail class.

    Methods:
        __init__ -> Initialize configuration environment.
        add_2_msg -> Stub holder for Mail.add_2_msg method.
        send_mail -> Stub holder for Mail.send_mail method.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the LoggerTest class.

        Arguments:

        """

        pass

    def add_2_msg(self, data):

        """Method:  add_2_msg

        Description:  Stub holder for Mail.add_2_msg method.

        Arguments:
            (input) data -> Data string.

        """

        pass

    def send_mail(self):

        """Method:  send_mail

        Description:  Stub holder for Mail.send_mail method.

        Arguments:

        """

        pass

def setup_mail(self, address, subject):

    """Method:  setup_mail

    Description:  Stub holder for gen_class.setup_mail function.

    Arguments:
        (input) address -> Email address.
        (input) subject -> Subject line.

    """

    return MailTest()

class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_status_true -> Test with status set to True.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class LoggerTest(object):

            """Class:  LoggerTest

            Description:  Class which is a representation of a Logger class.

            Methods:
                __init__ -> Initialize configuration environment.
                log_info -> Stub holder for Logger.log_info method.
                log_err -> Stub holder for Logger.log_err method.

            """

            def __init__(self, name, filename, logtype, logformat, dateformat):

                """Method:  __init__

                Description:  Initialization instance of the LoggerTest class.

                Arguments:
                    (input) name -> Name of logger instance.
                    (input) filename -> Log file name.
                    (input) logtype -> Level of reporting.
                    (input) logformat -> Format of the log entry.
                    (input) dateformat -> Datetime format.

                """

                pass

            def log_info(self, data):

                """Method:  log_info

                Description:  Stub holder for Logger.log_info method.

                Arguments:
                    (input) data -> Data string.

                """

                pass

            def log_err(self, data):

                """Method:  log_err

                Description:  Stub holder for Logger.log_err method.

                Arguments:
                    (input) data -> Data string.

                """

                pass

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.docid_dir = "/dir/path/docid_dir"
                self.admin_email = "name@domain"
                self.log_file = "/dir/path/log_file"

        self.cfg = CfgTest()
        self.log = LoggerTest()
        self.setupmail = setup_mail
        self.args_array = {"-c": "configfile", "-d": "/dir/config"}

    @mock.patch("pulled_search.validate_dirs", mock.Mock(return_value={}))
    @mock.patch("pulled_search.gen_libs.chk_crt_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.load_module")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_status_true(self, mock_log, mock_cfg):

        """Function:  test_status_true

        Description:  Test with status set to True.

        Arguments:

        """

        mock_log.return_value = self.log
        mock_cfg.return_value = self.cfg

        self.assertFalse(pulled_search.run_program(self.args_array))


if __name__ == "__main__":
    unittest.main()
