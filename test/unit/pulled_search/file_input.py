# Classification (U)

"""Program:  file_input.py

    Description:  Unit testing of file_input in pulled_search.py.

    Usage:
        test/unit/pulled_search/file_input.py

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


class ArgParser():                                      # pylint:disable=R0903

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class CfgTest():                                        # pylint:disable=R0903

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

        self.processed_file = "/dir/path/processed_dir/processed_file.txt"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_duplicate_docid
        test_multiple_docids
        test_no_docid
        test_single_docid
        test_failed_dict
        test_no_failed_dict
        test_update_process
        test_no_update_process

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.args_array = {"-F": "/dir_path/input_file"}
        docid = "09docid1 eucom 20230212 20230325"
        self.file_list = []
        self.file_list2 = [docid]
        self.file_list3 = [docid, "09docid2 eucom 20230214 20230401"]
        self.file_list4 = [docid, docid]
        self.docid_dict = {}
        self.docid_dict2 = {
            "09docid1": {
                "command": "eucom",
                "pubdate": "20230212",
                "pulldate": "20230401"}}
        self.docid_dict3 = {
            "09docid1": {
                "command": "eucom",
                "pubdate": "20230212",
                "pulldate": "20230401"},
            "09docid2": {
                "command": "eucom",
                "pubdate": "20230214",
                "pulldate": "20230401"}}
        self.failed_dict = []
        self.failed_dict2 = {"09docid1": "error_message"}

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.recall_search2")
    @mock.patch("pulled_search.remove_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_duplicate_docid(self, mock_log, mock_remove, mock_recall,
                             mock_list):

        """Function:  test_duplicate_docid

        Description:  Test with duplicate docid.

        Arguments:

        """

        mock_remove.return_value = self.docid_dict2
        mock_recall.return_value = self.failed_dict
        mock_list.return_value = self.file_list4

        self.assertFalse(
            pulled_search.file_input(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.recall_search2")
    @mock.patch("pulled_search.remove_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_docids(self, mock_log, mock_remove, mock_recall,
                             mock_list):

        """Function:  test_multiple_docids

        Description:  Test with multiple docids.

        Arguments:

        """

        mock_remove.return_value = self.docid_dict3
        mock_recall.return_value = self.failed_dict
        mock_list.return_value = self.file_list3

        self.assertFalse(
            pulled_search.file_input(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.recall_search2")
    @mock.patch("pulled_search.remove_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_no_docid(self, mock_log, mock_remove, mock_recall, mock_list):

        """Function:  test_no_docid

        Description:  Test with no docids in input file.

        Arguments:

        """

        mock_remove.return_value = self.docid_dict
        mock_recall.return_value = self.failed_dict
        mock_list.return_value = self.file_list

        self.assertFalse(
            pulled_search.file_input(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.recall_search2")
    @mock.patch("pulled_search.remove_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_docid(self, mock_log, mock_remove, mock_recall, mock_list):

        """Function:  test_single_docid

        Description:  Test with single docid.

        Arguments:

        """

        mock_remove.return_value = self.docid_dict2
        mock_recall.return_value = self.failed_dict
        mock_list.return_value = self.file_list2

        self.assertFalse(
            pulled_search.file_input(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.process_failed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.recall_search2")
    @mock.patch("pulled_search.remove_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_failed_dict(self, mock_log, mock_remove, mock_recall, mock_list):

        """Function:  test_failed_dict

        Description:  Test with failed_dict with failed files.

        Arguments:

        """

        mock_remove.return_value = self.docid_dict2
        mock_recall.return_value = self.failed_dict2
        mock_list.return_value = self.file_list2

        self.assertFalse(
            pulled_search.file_input(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.recall_search2")
    @mock.patch("pulled_search.remove_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_no_failed_dict(self, mock_log, mock_remove, mock_recall,
                            mock_list):

        """Function:  test_no_failed_dict

        Description:  Test with failed_dict with no failed files.

        Arguments:

        """

        mock_remove.return_value = self.docid_dict2
        mock_recall.return_value = self.failed_dict
        mock_list.return_value = self.file_list2

        self.assertFalse(
            pulled_search.file_input(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.recall_search2")
    @mock.patch("pulled_search.remove_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_update_process(self, mock_log, mock_remove, mock_recall,
                            mock_list):

        """Function:  test_update_process

        Description:  Test with update_process called.

        Arguments:

        """

        mock_remove.return_value = self.docid_dict2
        mock_recall.return_value = self.failed_dict
        mock_list.return_value = self.file_list2

        self.assertFalse(
            pulled_search.file_input(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.recall_search2")
    @mock.patch("pulled_search.remove_processed")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_no_update_process(self, mock_log, mock_remove, mock_recall,
                               mock_list):

        """Function:  test_no_update_process

        Description:  Test with no update_process called.

        Arguments:

        """

        mock_remove.return_value = self.docid_dict
        mock_recall.return_value = self.failed_dict
        mock_list.return_value = self.file_list2

        self.assertFalse(
            pulled_search.file_input(self.args, self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
