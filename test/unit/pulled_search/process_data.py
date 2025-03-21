# Classification (U)

"""Program:  process_data.py

    Description:  Unit testing of process_data in pulled_search.py.

    Usage:
        test/unit/pulled_search/process_data.py

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
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_file_not_exist
        test_file_empty
        test_process_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.ofile = "/path/file_name_processed"
        self.server = "server_name"
        self.log_json = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE",
            "asOf": "20230306 084503", "servers": {}}
        self.fname = "Log_File_Name"
        self.file_log = ["Line1", "Line2", "Line3"]
        self.docid_dict = {"docid": "09109uosdhf", "command": "COMMAND",
                           "pubdate": "20200102-101134"}
        self.docid_dict2 = {"docid": "09109uosdhf", "command": "intelink",
                            "pubdate": "20200102-101134"}
        self.docid_dict3 = {"docid": "09109uosdhf", "command": "COMMAND",
                            "pubdate": "20200102-101134",
                            "pulldate": "20230426"}
        self.results = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE",
            "asOf": "20230306 084503",
            "servers": {"server_name": ["Line1", "Line2", "Line3"]}}
        self.results2 = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE",
            "asOf": "20230306 084503",
            "servers": {}}

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_file_not_exist(self, mock_log):

        """Function:  test_file_not_exist

        Description:  Test with file not existing.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_data(
            self.ofile, self.log_json, self.fname, self.server,
            mock_log), self.results2)

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_file_empty(self, mock_log):

        """Function:  test_file_empty

        Description:  Test with empty file.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_data(
            self.ofile, self.log_json, self.fname, self.server,
            mock_log), self.results2)

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_process_data(self, mock_log, mock_list):

        """Function:  test_process_data

        Description:  Test with processing data.

        Arguments:

        """

        mock_log.return_value = True
        mock_list.return_value = self.file_log

        self.assertEqual(pulled_search.process_data(
            self.ofile, self.log_json, self.fname, self.server,
            mock_log), self.results)


if __name__ == "__main__":
    unittest.main()
