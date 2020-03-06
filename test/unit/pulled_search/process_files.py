#!/usr/bin/python
# Classification (U)

"""Program:  process_files.py

    Description:  Unit testing of process_files in pulled_search.py.

    Usage:
        test/unit/pulled_search/process_files.py

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

                self.file_regex = "*_docid.json"
                self.docid_dir = "/dir_path/docid_dir"
                self.error_dir = "/dir/path/error_dir"

        self.cfg = CfgTest()
        self.log_files = ["/path/logfile1", "/path/logfile2"]
        self.args_array = {"-t": "name@domain"}

    @mock.patch("pulled_search.gen_libs.dir_file_match")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_no_log_files(self, mock_log, mock_match):

        """Function:  test_no_log_files

        Description:  Test with no log files detected.

        Arguments:

        """

        mock_log.return_value = True
        mock_match.return_value = []

        self.assertFalse(pulled_search.process_files({}, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value="MailInstance"))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.dir_file_match")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_mail(self, mock_log, mock_match):

        """Function:  test_with_mail

        Description:  Test with mail setup.

        Arguments:

        """

        mock_log.return_value = True
        mock_match.return_value = self.log_files

        self.assertFalse(pulled_search.process_files(self.args_array self.cfg,
                                                     mock_log))

    @mock.patch("pulled_search.non_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.dir_file_match")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_data(self, mock_log, mock_match):

        """Function:  test_with_data

        Description:  Test with successful log file check.

        Arguments:

        """

        mock_log.return_value = True
        mock_match.return_value = self.log_files

        self.assertFalse(pulled_search.process_files({}, self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
