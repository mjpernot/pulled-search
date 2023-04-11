# Classification (U)

"""Program:  recall_search.py

    Description:  Unit testing of recall_search in pulled_search.py.

    Usage:
        test/unit/pulled_search/recall_search.py

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
        test_pattern_found
        test_no_pattern
        test_missing_file
        test_empty_file
        test_multiple_file_dict
        test_single_file_dict
        test_empty_file_dict

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.docid = "090109abcdef"
        self.docid2 = "090109fedcba"
        self.fhtml = "CMD-LEV-PULLED-20221102-0000-GEN-LEV2-090109abcdef.html"
        self.fhtml2 = "CMD-LEV-PULLED-20230102-0000-GEN-LEV-090109fedcba.html"
        self.basepath = "test/unit/pulled_search/testfiles"
        self.fname0 = os.path.join(self.basepath, "test_recall_search0.txt")
        self.fname = os.path.join(self.basepath, "test_recall_search.txt")
        self.fname2 = os.path.join(self.basepath, "test_recall_search2.txt")
        self.fname3 = os.path.join(self.basepath, self.fhtml)
        self.fname4 = os.path.join(self.basepath, self.fhtml2)
        self.file_dict = {}
        self.file_dict2 = {self.docid: self.fname2}
        self.file_dict3 = {self.docid: self.fname2, self.docid2: self.fname4}
        self.file_dict4 = {self.docid: self.fname}
        self.file_dict5 = {self.docid: self.fname0}
        self.file_dict6 = {self.docid: self.fname3}
        self.results = dict()
        self.results2 = {self.docid: "No such file or directory"}
        self.results3 = {self.docid: "Failed the process_docid process"}
        self.docid_results = dict()
        self.docid_results2 = {self.docid: "Failed the process_docid process"}
        

    @mock.patch("pulled_search.search_docid")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_process_docid_passed(self, mock_log, mock_docid):

        """Function:  test_process_docid_passed

        Description:  Test with the process_docid passing.

        Arguments:

        """

        mock_docid.return_value = self.docid_results

        self.assertEqual(
            pulled_search.recall_search(
                self.args, self.cfg, mock_log, self.file_dict6), self.results)

    @mock.patch("pulled_search.search_docid")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_process_docid_failed(self, mock_log, mock_docid):

        """Function:  test_process_docid_failed

        Description:  Test with the process_docid failing.

        Arguments:

        """

        mock_docid.return_value = self.docid_results2

        self.assertEqual(
            pulled_search.recall_search(
                self.args, self.cfg, mock_log, self.file_dict6), self.results3)

    @mock.patch("pulled_search.search_docid")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_pattern_found(self, mock_log, mock_docid):

        """Function:  test_pattern_found

        Description:  Test with pattern found.

        Arguments:

        """

        mock_docid.return_value = self.docid_results

        self.assertEqual(
            pulled_search.recall_search(
                self.args, self.cfg, mock_log, self.file_dict6), self.results)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_no_pattern(self, mock_log):

        """Function:  test_no_pattern

        Description:  Test with no pattern found.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search(
                self.args, self.cfg, mock_log, self.file_dict2), self.results)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_missing_file(self, mock_log):

        """Function:  test_missing_file

        Description:  Test with missing file.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search(
                self.args, self.cfg, mock_log, self.file_dict5), self.results2)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_empty_file(self, mock_log):

        """Function:  test_empty_file

        Description:  Test with empty file.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search(
                self.args, self.cfg, mock_log, self.file_dict4), self.results)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_file_dict(self, mock_log):

        """Function:  test_multiple_file_dict

        Description:  Test with multiple file in file_dict.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search(
                self.args, self.cfg, mock_log, self.file_dict3), self.results)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_file_dict(self, mock_log):

        """Function:  test_single_file_dict

        Description:  Test with single file in file_dict.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search(
                self.args, self.cfg, mock_log, self.file_dict2), self.results)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_empty_file_dict(self, mock_log):

        """Function:  test_empty_file_dict

        Description:  Test with empty file_dict.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search(
                self.args, self.cfg, mock_log, self.file_dict), self.results)


if __name__ == "__main__":
    unittest.main()
