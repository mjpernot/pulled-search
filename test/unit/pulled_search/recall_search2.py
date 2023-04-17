# Classification (U)

"""Program:  recall_search2.py

    Description:  Unit testing of recall_search2 in pulled_search.py.

    Usage:
        test/unit/pulled_search/recall_search2.py

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

        self.doc_dir = ["/dir_path/doc_dir"]
        self.pattern = "JAC.pull.subtype.*.SECURITY RECALL"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_process_docid_passed
        test_process_docid_failed
        test_multiple_docid_dict
        test_single_docid_dict
        test_empty_docid_dict

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        docid = "090109abcdef"
        docid2 = "090109fedcba"
        self.docid_dict = {}
        self.docid_dict2 = {docid: {"command": "eucom", "pubdate": "20230417"}}
        self.docid_dict3 = {docid: {
            "command": "eucom", "pubdate": "20230417",
            "command": "socom", "pubdate": "20230120"}}
        self.results = dict()
        self.results2 = {docid: "Failed the process_docid process"}
        self.docid_results = dict()
        self.docid_results2 = {docid: "Failed the process_docid process"}
        

    @mock.patch("pulled_search.search_docid", mock.Mock(return_value=dict()))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_process_docid_passed(self, mock_log):

        """Function:  test_process_docid_passed

        Description:  Test with the process_docid passing.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search2(
                self.args, self.cfg, mock_log, self.docid_dict2), self.results)

    @mock.patch("pulled_search.search_docid")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_process_docid_failed(self, mock_log, mock_docid):

        """Function:  test_process_docid_failed

        Description:  Test with the process_docid failing.

        Arguments:

        """

        mock_docid.return_value = self.docid_results2

        self.assertEqual(
            pulled_search.recall_search2(
                self.args, self.cfg, mock_log, self.docid_dict2),
            self.results2)

    @mock.patch("pulled_search.search_docid", mock.Mock(return_value=dict()))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_docid_dict(self, mock_log):

        """Function:  test_multiple_docid_dict

        Description:  Test with multiple file in file_dict.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search2(
                self.args, self.cfg, mock_log, self.docid_dict3), self.results)

    @mock.patch("pulled_search.search_docid", mock.Mock(return_value=dict()))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_docid_dict(self, mock_log):

        """Function:  test_single_docid_dict

        Description:  Test with single file in file_dict.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search2(
                self.args, self.cfg, mock_log, self.docid_dict2), self.results)

    @mock.patch("pulled_search.search_docid", mock.Mock(return_value=dict()))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_empty_docid_dict(self, mock_log):

        """Function:  test_empty_docid_dict

        Description:  Test with empty file_dict.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search2(
                self.args, self.cfg, mock_log, self.docid_dict), self.results)


if __name__ == "__main__":
    unittest.main()
