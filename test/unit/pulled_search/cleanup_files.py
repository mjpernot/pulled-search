#!/usr/bin/python
# Classification (U)

"""Program:  cleanup_files.py

    Description:  Unit testing of cleanup_files in pulled_search.py.

    Usage:
        test/unit/pulled_search/cleanup_files.py

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
        test_multiple_item_list -> Test multiple entries in processed list.
        test_single_item_list2 -> Test with multiple entries in processed list.
        test_single_item_list -> Test with multiple entries in processed list.
        test_empty_list -> Test with an empty processed list.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.docid_files = ["/path/docidfile1"]
        self.docid_files2 = ["/path/docidfile1", "/path/docidfile2"]
        self.docid_files3 = ["/path/docidfile1", "/path/docidfile2",
                             "/path/docidfile3"]
        self.processed_list = ["/path/docidfile1"]
        self.processed_list2 = ["/path/docidfile1", "/path/docidfile2"]
        self.dest_dir = "/path/dest_dir"
        self.results = ["/path/docidfile2"]
        self.results2 = ["/path/docidfile3"]
        self.results3 = ["/path/docidfile1"]

    @mock.patch("pulled_search.gen_libs.mv_file2",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_item_list(self, mock_log):

        """Function:  test_multiple_item_list

        Description:  Test with multiple entries in processed list.

        Arguments:

        """

        mock_log.return_value = "Log Instance"

        self.assertEqual(pulled_search.cleanup_files(
            self.docid_files3, self.processed_list2, self.dest_dir, mock_log),
            self.results2)

    @mock.patch("pulled_search.gen_libs.mv_file2",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_item_list2(self, mock_log):

        """Function:  test_single_item_list2

        Description:  Test with one entry in processed list.

        Arguments:

        """

        mock_log.return_value = "Log Instance"

        self.assertEqual(pulled_search.cleanup_files(
            self.docid_files2, self.processed_list, self.dest_dir, mock_log),
            self.results)

    @mock.patch("pulled_search.gen_libs.mv_file2",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_item_list(self, mock_log):

        """Function:  test_single_item_list

        Description:  Test with one entry in processed list.

        Arguments:

        """

        mock_log.return_value = "Log Instance"

        self.assertEqual(pulled_search.cleanup_files(
            self.docid_files, self.processed_list, self.dest_dir, mock_log),
            [])

    @mock.patch("pulled_search.gen_class.Logger")
    def test_empty_list(self, mock_log):

        """Function:  test_empty_list

        Description:  Test with an empty processed file list.

        Arguments:

        """

        mock_log.return_value = "Log Instance"

        self.assertEqual(pulled_search.cleanup_files(
            self.docid_files, [], self.dest_dir, mock_log), self.results3)


if __name__ == "__main__":
    unittest.main()
