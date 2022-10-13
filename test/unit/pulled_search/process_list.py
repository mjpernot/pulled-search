# Classification (U)

"""Program:  process_list.py

    Description:  Unit testing of process_list in pulled_search.py.

    Usage:
        test/unit/pulled_search/process_list.py

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

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()


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

        self.file_regex = "*_docid.json"
        self.doc_dir = "/dir_path/doc_dir"
        self.error_dir = "/dir/path/error_dir"
        self.archive_dir = "/dir/path/archive_dir"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_incorrect_action
        test_fails_item_list2 -> Test with some failures in insert file list
        test_multiple_item_list2
        test_single_item_list2
        test_fails_item_list -> Test with some failures in search file list
        test_multiple_item_list
        test_single_item_list
        test_empty_list

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args.args_array = {"-t": "name@domain"}
        self.cfg = CfgTest()
        self.docid1 = "/path/docidfile1"
        self.docid2 = "/path/docidfile2"
        self.docid_files = [self.docid1]
        self.docid_files2 = [self.docid1, self.docid2]
        self.results = [self.docid1]
        self.results2 = [self.docid1, self.docid2]
        self.results3 = [self.docid2]
        self.action = "search"
        self.action2 = "insert"
        self.action3 = "badaction"

    @mock.patch("pulled_search.gen_class.Logger")
    def test_incorrect_action(self, mock_log):

        """Function:  test_incorrect_action

        Description:  Test with incorrect action passed.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_list(
            self.args, self.cfg, mock_log, self.docid_files2,
            self.action3), [])

    @mock.patch("pulled_search.process_insert",
                mock.Mock(side_effect=[False, True]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_fails_item_list2(self, mock_log):

        """Function:  test_fails_item_list2

        Description:  Test with multiple entries in insert file list.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_list(
            self.args, self.cfg, mock_log, self.docid_files2,
            self.action2), self.results3)

    @mock.patch("pulled_search.process_insert", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_item_list2(self, mock_log):

        """Function:  test_multiple_item_list2

        Description:  Test with multiple entries in insert file list.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_list(
            self.args, self.cfg, mock_log, self.docid_files2,
            self.action2), self.results2)

    @mock.patch("pulled_search.process_insert", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_item_list2(self, mock_log):

        """Function:  test_single_item_list2

        Description:  Test with one entry in insert file list.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_list(
            self.args, self.cfg, mock_log, self.docid_files,
            self.action2), self.results)

    @mock.patch("pulled_search.process_docid",
                mock.Mock(side_effect=[False, True]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_fails_item_list(self, mock_log):

        """Function:  test_fails_item_list

        Description:  Test with multiple entries in search file list.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_list(
            self.args, self.cfg, mock_log, self.docid_files2,
            self.action), self.results3)

    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_item_list(self, mock_log):

        """Function:  test_multiple_item_list

        Description:  Test with multiple entries in search file list.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_list(
            self.args, self.cfg, mock_log, self.docid_files2,
            self.action), self.results2)

    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_item_list(self, mock_log):

        """Function:  test_single_item_list

        Description:  Test with one entry in search file list.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_list(
            self.args, self.cfg, mock_log, self.docid_files,
            self.action), self.results)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_empty_list(self, mock_log):

        """Function:  test_empty_list

        Description:  Test with an empty docid file list.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_list(
            self.args, self.cfg, mock_log, [], self.action), [])


if __name__ == "__main__":
    unittest.main()
