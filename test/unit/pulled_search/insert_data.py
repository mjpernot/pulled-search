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
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_nonprocessed_files -> Test with nonprocessed files.
        test_no_log_files -> Test with no log files detected.
        test_with_mail -> Test with mail setup.
        test_with_data -> Test with successful log file check.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

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

                self.file_regex2 = "*_insert.json"
                self.monitor_dir = "/dir_path/monitor_dir"
                self.error_dir = "/dir/path/error_dir"
                self.archive_dir = "/dir/path/archive_dir"

        self.cfg = CfgTest()
        self.args_array = {"-t": "name@domain"}

    @mock.patch("pulled_search.setup_mail", mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_list", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.dir_file_search", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_nonprocessed_files(self, mock_log):

        """Function:  test_nonprocessed_files

        Description:  Test with nonprocessed files.

        Arguments:

        """

        self.assertFalse(pulled_search.insert_data({}, self.cfg, mock_log))

    @mock.patch("pulled_search.setup_mail", mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_list", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.dir_file_search", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_no_log_files(self, mock_log):

        """Function:  test_no_log_files

        Description:  Test with no log files detected.

        Arguments:

        """

        self.assertFalse(pulled_search.insert_data({}, self.cfg, mock_log))

    @mock.patch("pulled_search.setup_mail", mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_list", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.dir_file_search", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_mail(self, mock_log):

        """Function:  test_with_mail

        Description:  Test with mail setup.

        Arguments:

        """

        mock_log.return_value = True

        self.assertFalse(pulled_search.insert_data(self.args_array, self.cfg,
                                                     mock_log))

    @mock.patch("pulled_search.setup_mail", mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_list", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.dir_file_search", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_data(self, mock_log):

        """Function:  test_with_data

        Description:  Test with successful log file check.

        Arguments:

        """

        self.assertFalse(pulled_search.insert_data({}, self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
