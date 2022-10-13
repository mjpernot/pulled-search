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
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_multiple_item_list
        test_single_item_list2
        test_single_item_list
        test_empty_list

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.docid1 = "/path/docidfile1"
        self.docid2 = "/path/docidfile2"
        self.docid_files = [self.docid1]
        self.docid_files2 = [self.docid1, self.docid2]
        self.docid_files3 = [self.docid1, self.docid2,
                             "/path/docidfile3"]
        self.processed_list = [self.docid1]
        self.processed_list2 = [self.docid1, self.docid2]
        self.dest_dir = "/path/dest_dir"
        self.results = [self.docid2]
        self.results2 = ["/path/docidfile3"]
        self.results3 = [self.docid1]
        self.loginst = "Log Instance"

    @mock.patch("pulled_search.gen_libs.mv_file2",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_item_list(self, mock_log):

        """Function:  test_multiple_item_list

        Description:  Test with multiple entries in processed list.

        Arguments:

        """

        mock_log.return_value = self.loginst

        self.assertEqual(
            pulled_search.cleanup_files(
                self.docid_files3, self.processed_list2, self.dest_dir,
                mock_log), self.results2)

    @mock.patch("pulled_search.gen_libs.mv_file2",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_item_list2(self, mock_log):

        """Function:  test_single_item_list2

        Description:  Test with one entry in processed list.

        Arguments:

        """

        mock_log.return_value = self.loginst

        self.assertEqual(
            pulled_search.cleanup_files(
                self.docid_files2, self.processed_list, self.dest_dir,
                mock_log), self.results)

    @mock.patch("pulled_search.gen_libs.mv_file2",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_item_list(self, mock_log):

        """Function:  test_single_item_list

        Description:  Test with one entry in processed list.

        Arguments:

        """

        mock_log.return_value = self.loginst

        self.assertEqual(
            pulled_search.cleanup_files(
                self.docid_files, self.processed_list, self.dest_dir,
                mock_log), [])

    @mock.patch("pulled_search.gen_class.Logger")
    def test_empty_list(self, mock_log):

        """Function:  test_empty_list

        Description:  Test with an empty processed file list.

        Arguments:

        """

        mock_log.return_value = self.loginst

        self.assertEqual(pulled_search.cleanup_files(
            self.docid_files, [], self.dest_dir, mock_log), self.results3)


if __name__ == "__main__":
    unittest.main()
