# Classification (U)

"""Program:  remove_processed.py

    Description:  Unit testing of remove_processed in pulled_search.py.

    Usage:
        test/unit/pulled_search/remove_processed.py

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
import pulled_search
import version

__version__ = version.__version__


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

        self.file_regex = "*.-PULLED-.*.html"
        self.doc_dir = ["/dir_path/doc_dir"]
        self.processed_file = "/dir/path/processed_dir/processed_file.txt"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_processed_docids_dupes
        test_processed_docids_exist
        test_processed_file_none

    """


    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.docid_files = {"09docid": "metadata", "09docid2": "metadata",
                            "09docid3": "metadata"}
        self.processed_file = list()
        self.processed_file2 = ["09docid4"]
        self.processed_file3 = ["09docid2"]
        self.results = {"09docid": "metadata", "09docid2": "metadata",
                        "09docid3": "metadata"}
        self.results2 = {"09docid": "metadata", "09docid3": "metadata"}

    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_processed_docids_dupes(self, mock_log, mock_load):

        """Function:  test_processed_docids_dupes

        Description:  Test with dupe processed docids.

        Arguments:

        """

        mock_load.return_value = self.processed_file3

        self.assertEqual(
            pulled_search.remove_processed(
                self.cfg, mock_log, self.docid_files), self.results2)

    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_processed_docids_exist(self, mock_log, mock_load):

        """Function:  test_processed_docids_exist

        Description:  Test with existing processed docids.

        Arguments:

        """

        mock_load.return_value = self.processed_file2

        self.assertEqual(
            pulled_search.remove_processed(
                self.cfg, mock_log, self.docid_files), self.results)

    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_processed_docids_none(self, mock_log, mock_load):

        """Function:  test_processed_docids_none

        Description:  Test with no processed docids.

        Arguments:

        """

        mock_load.return_value = self.processed_file

        self.assertEqual(
            pulled_search.remove_processed(
                self.cfg, mock_log, self.docid_files), self.results)


if __name__ == "__main__":
    unittest.main()
