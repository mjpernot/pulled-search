#!/usr/bin/python
# Classification (U)

"""Program:  process_insert.py

    Description:  Unit testing of process_insert in pulled_search.py.

    Usage:
        test/unit/pulled_search/process_insert.py

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

                self.db = "databasename"
                self.tbl = "tablename"

        self.cfg = CfgTest()
        self.args_array = {"-d": "/config_path"}
        self.data_list = ['{',
                          '"docID": "weotiuer",',
                          '"command": "COMMAND",',
                          '"pubDate": "20200102-101134",',
                          '"securityEnclave": "ENCLAVE",',
                          '"asOf": "20200306 084503",',
                          '"serverName": "SERVERNAME",',
                          '"logEntries": ["line1", "line2", "line3"]',
                          '}']
        self.fname = "/dir_path/092438k234_insert.json"

    @mock.patch("pulled_search.json.loads", mock.Mock(return_value="String"))
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_json_failure(self, mock_log, mock_list):

        """Function:  test_json_failure

        Description:  Test with conversion to JSON failure.

        Arguments:

        """

        mock_log.return_value = True
        mock_list.return_value = self.data_list

        self.assertEqual(pulled_search.process_insert(
            self.args_array, self.cfg, self.fname, mock_log), False)

    @mock.patch("pulled_search.mongo_libs.ins_doc",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_data(self, mock_log, mock_list):

        """Function:  test_with_data

        Description:  Test with successful log file check.

        Arguments:

        """

        mock_log.return_value = True
        mock_list.return_value = self.data_list

        self.assertEqual(pulled_search.process_insert(
            self.args_array, self.cfg, self.fname, mock_log), True)


if __name__ == "__main__":
    unittest.main()
