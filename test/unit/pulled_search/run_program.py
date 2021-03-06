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


def process_files(args_array, cfg, log):

    """Function:  process_files

    Description:  This is a function stub for pulled_search.process_files.

    Arguments:
        (input) args_array -> Dictionary of command line options and values.
        (input) cfg -> Configuration setup.
        (input) log -> Log class instance.

    """

    status = True

    if args_array and cfg and log:
        status = True

    return status


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_validation_failure -> Test with directory validation failure.
        test_status_false -> Test with status set to False.
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

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the LoggerTest class.

                Arguments:

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
                self.log_file = "/dir/path/log_file"

        self.cfg = CfgTest()
        self.log = LoggerTest()
        self.func_dict = {"-P": process_files}
        self.dircfg = "/dir/config"
        self.args_array = {"-c": "configfile", "-d": self.dircfg}
        self.args_array2 = {"-c": "configfile", "-d": self.dircfg,
                            "-m": "/dir/newdir"}
        self.args_array3 = {"-c": "configfile", "-d": self.dircfg,
                            "-P": True}

    @mock.patch("pulled_search.checks_dirs", mock.Mock(
        return_value={"/dir_path/doc_dir": "Doc_dir failure"}))
    @mock.patch("pulled_search.gen_libs.chk_crt_dir",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.config_override")
    @mock.patch("pulled_search.gen_libs.load_module")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_validation_failure(self, mock_log, mock_cfg, mock_override):

        """Function:  test_validation_failure

        Description:  Test with directory validation failure.

        Arguments:

        """

        mock_log.return_value = self.log
        mock_cfg.return_value = self.cfg
        mock_override.return_value = self.cfg

        self.assertFalse(pulled_search.run_program(self.args_array,
                                                   self.func_dict))

    @mock.patch("pulled_search.gen_libs.chk_crt_dir",
                mock.Mock(return_value=(False, "Error Message")))
    @mock.patch("pulled_search.config_override")
    @mock.patch("pulled_search.gen_libs.load_module")
    def test_status_false(self, mock_cfg, mock_override):

        """Function:  test_status_false

        Description:  Test with status set to False.

        Arguments:

        """

        mock_cfg.return_value = self.cfg
        mock_override.return_value = self.cfg

        with gen_libs.no_std_out():
            self.assertFalse(pulled_search.run_program(self.args_array,
                                                       self.func_dict))

    @mock.patch("pulled_search.checks_dirs", mock.Mock(return_value={}))
    @mock.patch("pulled_search.gen_libs.chk_crt_dir",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.config_override")
    @mock.patch("pulled_search.gen_libs.load_module")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_status_true(self, mock_log, mock_cfg, mock_override):

        """Function:  test_status_true

        Description:  Test with status set to True.

        Arguments:

        """

        mock_log.return_value = self.log
        mock_cfg.return_value = self.cfg
        mock_override.return_value = self.cfg

        self.assertFalse(pulled_search.run_program(self.args_array3,
                                                   self.func_dict))


if __name__ == "__main__":
    unittest.main()
