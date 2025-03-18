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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import pulled_search                            # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


def process_files(args_array, cfg, log):

    """Function:  process_files

    Description:  This is a function stub for pulled_search.process_files.

    Arguments:

    """

    status = True

    if args_array and cfg and log:
        status = True

    return status


class ArgParser():

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val
        get_args_keys

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)

    def get_args_keys(self):

        """Method:  get_args_keys

        Description:  Method stub holder for gen_class.ArgParser.get_args_keys.

        Arguments:

        """

        return list(self.args_array.keys())


class LoggerTest():

    """Class:  LoggerTest

    Description:  Class which is a representation of a Logger class.

    Methods:
        __init__
        log_info
        log_err

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the LoggerTest class.

        Arguments:

        """

    def log_info(self, data):

        """Method:  log_info

        Description:  Stub holder for Logger.log_info method.

        Arguments:

        """

    def log_err(self, data):

        """Method:  log_err

        Description:  Stub holder for Logger.log_err method.

        Arguments:

        """


class CfgTest():                                        # pylint:disable=R0903

    """Class:  CfgTest

    Description:  Class which is a representation of a cfg module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.docid_dir = "/dir/path/docid_dir"
        self.log_file = "/dir/path/log_file"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_validation_failure
        test_status_false
        test_status_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.log = LoggerTest()
        self.func_list = {"-P": process_files}
        self.dircfg = "/dir/config"
        self.args_array = {"-c": "configfile", "-d": self.dircfg}
        self.args_array2 = {"-c": "configfile", "-d": self.dircfg, "-P": True}

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

        self.args.args_array = self.args_array

        mock_log.return_value = self.log
        mock_cfg.return_value = self.cfg
        mock_override.return_value = self.cfg

        self.assertFalse(pulled_search.run_program(self.args, self.func_list))

    @mock.patch("pulled_search.gen_libs.chk_crt_dir",
                mock.Mock(return_value=(False, "Error Message")))
    @mock.patch("pulled_search.config_override")
    @mock.patch("pulled_search.gen_libs.load_module")
    def test_status_false(self, mock_cfg, mock_override):

        """Function:  test_status_false

        Description:  Test with status set to False.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_cfg.return_value = self.cfg
        mock_override.return_value = self.cfg

        with gen_libs.no_std_out():
            self.assertFalse(
                pulled_search.run_program(self.args, self.func_list))

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

        self.args.args_array = self.args_array2

        mock_log.return_value = self.log
        mock_cfg.return_value = self.cfg
        mock_override.return_value = self.cfg

        self.assertFalse(pulled_search.run_program(self.args, self.func_list))


if __name__ == "__main__":
    unittest.main()
