#!/usr/bin/python
# Classification (U)

"""Program:  insert_data.py

    Description:  Unit testing of insert_data in pulled_search.py.

    Usage:
        test/unit/pulled_search/insert_data.py

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
import version

__version__ = version.__version__


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class CfgTest(object):

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

        self.mfile_regex = "*_insert.json"
        self.monitor_dir = "/dir_path/monitor_dir"
        self.merror_dir = "/dir/path/error_dir"
        self.marchive_dir = "/dir/path/archive_dir"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_with_preamble
        test_with_no_mail
        test_nonprocessed_files
        test_no_log_files
        test_with_mail
        test_with_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.args_array = {"-t": "name@domain"}
        self.args_array2 = {}
        self.args_array3 = {"-t": "name@domain", "-s": "Pre-amble: "}

    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_list", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_preamble(self, mock_log):

        """Function:  test_with_preamble

        Description:  Test with pre-amble subject.

        Arguments:

        """

        self.args.args_array = self.args_array3

        mock_log.return_value = True

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_list", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_no_mail(self, mock_log):

        """Function:  test_with_no_mail

        Description:  Test with no mail setup.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_log.return_value = True

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_list", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_nonprocessed_files(self, mock_log):

        """Function:  test_nonprocessed_files

        Description:  Test with nonprocessed files.

        Arguments:

        """

        self.args.args_array = dict()

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_list", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_no_log_files(self, mock_log):

        """Function:  test_no_log_files

        Description:  Test with no log files detected.

        Arguments:

        """

        self.args.args_array = dict()

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_list", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_mail(self, mock_log):

        """Function:  test_with_mail

        Description:  Test with mail setup.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_list", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_data(self, mock_log):

        """Function:  test_with_data

        Description:  Test with successful log file check.

        Arguments:

        """

        self.args.args_array = dict()

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
