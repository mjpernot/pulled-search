#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in pulled_search.py.

    Usage:
        test/unit/pulled_search/main.py

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


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = cmdline
        self.flavor = flavor


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_help_true
        test_help_false
        test_require_true
        test_require_false
        test_con_req_or_false
        test_con_req_or_true
        test_dir_chk_crt_true
        test_dir_chk_crt_false
        test_xor_dict_false
        test_xor_dict_true
        test_run_program
        test_programlock_true
        test_programlock_false
        test_programlock_id

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = {"-c": "config_file", "-d": "config_dir", "-R": True}
        self.args2 = {"-c": "config_file", "-d": "config_dir", "-R": True,
                      "-y": "Flavor"}
        self.proglock = ProgramLock(["cmdline"], "FlavorID")

    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser.arg_parse2")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_help_true

        Description:  Test with help_func returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_help_false

        Description:  Test with help_func returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_require_true(self, mock_arg, mock_help):

        """Function:  test_require_true

        Description:  Test with arg_require returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_require_false(self, mock_arg, mock_help):

        """Function:  test_require_false

        Description:  Test with arg_require returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_cond_req_or.return_value = False

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_con_req_or_false(self, mock_arg, mock_help):

        """Function:  test_con_req_or_false

        Description:  Test with arg_cond_req_or returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_cond_req_or.return_value = False

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_con_req_or_true(self, mock_arg, mock_help):

        """Function:  test_con_req_or_true

        Description:  Test with arg_cond_req_or returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_xor_dict.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_dir_chk_crt_true(self, mock_arg, mock_help):

        """Function:  test_dir_chk_crt_true

        Description:  Test with arg_dir_chk_crt returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_cond_req_or.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_dir_chk_crt_false(self, mock_arg, mock_help):

        """Function:  test_dir_chk_crt_false

        Description:  Test with arg_dir_chk_crt returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_cond_req_or.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_xor_dict.return_value = False

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_xor_dict_false(self, mock_arg, mock_help):

        """Function:  test_xor_dict_false

        Description:  Test with arg_xor_dict returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_cond_req_or.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_xor_dict.return_value = False

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_class.ProgramLock")
    @mock.patch("pulled_search.run_program")
    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_xor_dict_true(self, mock_arg, mock_help, mock_run, mock_lock):

        """Function:  test_xor_dict_true

        Description:  Test with arg_xor_dict returns True.

        Arguments:

        """

        mock_lock.return_value = self.proglock
        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_cond_req_or.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_xor_dict.return_value = True
        mock_run.return_value = True

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_class.ProgramLock")
    @mock.patch("pulled_search.run_program")
    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_run_program(self, mock_arg, mock_help, mock_run, mock_lock):

        """Function:  test_run_program

        Description:  Test run_program function.

        Arguments:

        """

        mock_lock.return_value = self.proglock
        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_cond_req_or.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_xor_dict.return_value = True
        mock_run.return_value = True

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_class.ProgramLock")
    @mock.patch("pulled_search.run_program")
    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_programlock_true(self, mock_arg, mock_help, mock_run, mock_lock):

        """Function:  test_programlock_true

        Description:  Test with ProgramLock returns True.

        Arguments:

        """

        mock_lock.return_value = self.proglock
        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_cond_req_or.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_xor_dict.return_value = True
        mock_run.return_value = True

        self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_class.ProgramLock")
    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_programlock_false(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_false

        Description:  Test with ProgramLock returns False.

        Arguments:

        """

        mock_lock.side_effect = \
            pulled_search.gen_class.SingleInstanceException
        mock_arg.arg_parse2.return_value = self.args
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_cond_req_or.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False

        with gen_libs.no_std_out():
            self.assertFalse(pulled_search.main())

    @mock.patch("pulled_search.gen_class.ProgramLock")
    @mock.patch("pulled_search.run_program")
    @mock.patch("pulled_search.gen_libs.help_func")
    @mock.patch("pulled_search.arg_parser")
    def test_programlock_id(self, mock_arg, mock_help, mock_run, mock_lock):

        """Function:  test_programlock_id

        Description:  Test ProgramLock with flavor ID.

        Arguments:

        """

        mock_lock.return_value = self.proglock
        mock_arg.arg_parse2.return_value = self.args2
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_cond_req_or.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_xor_dict.return_value = True
        mock_run.return_value = True

        self.assertFalse(pulled_search.main())


if __name__ == "__main__":
    unittest.main()
