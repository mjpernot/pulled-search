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
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


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


class CfgTest2(object):

    """Class:  CfgTest2

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
        self.doc_dir = ["/dir_path/doc_dir", "/dir_path/doc_dir2"]
        self.processed_file = "/dir/path/processed_dir/processed_file.txt"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_failed_dict
        test_update_process
        test_processed_file_dupes
        test_processed_file_exist
        test_processed_file_none
        test_file_dict_dupes
        test_file_dict_no_dupes
        test_docid_files_multiple
        test_docid_files_single
        test_docid_files_empty
        test_search_dir_multiple
        test_search_dir_single
        test_arg_m_option

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.cfg2 = CfgTest2()
        self.args_array = {"-m": "/dir_path/doc_dir3"}
        self.docid_files = list()
        f_name = "/path/file1.html"
        self.docid_files2 = [f_name]
        self.docid_files3 = [f_name, "/path/file2.html"]
        self.docid_files4 = [f_name, f_name]
        self.processed_files = list()
        self.processed_files2 = ["file2.html"]
        self.failed_dict = list()
        self.failed_dict2 = {"file1.html": f_name}

    @mock.patch("pulled_search.process_failed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_failed_dict(self, mock_log, mock_search, mock_load, mock_recall):

        """Function:  test_failed_dict

        Description:  Test with failed_dict with failed files.

        Arguments:

        """

        mock_search.return_value = self.docid_files3
        mock_load.return_value = self.processed_files2
        mock_recall.return_value = self.failed_dict2

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_update_process(self, mock_log, mock_search, mock_load,
                            mock_recall):

        """Function:  test_update_process

        Description:  Test with update_process called.

        Arguments:

        """

        mock_search.return_value = self.docid_files3
        mock_load.return_value = self.processed_files2
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_processed_file_dupes(self, mock_log, mock_search, mock_load,
                                  mock_recall):

        """Function:  test_processed_file_dupes

        Description:  Test with dupe processed files.

        Arguments:

        """

        mock_search.return_value = self.docid_files3
        mock_load.return_value = self.processed_files2
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_processed_file_exist(self, mock_log, mock_search, mock_load,
                                  mock_recall):

        """Function:  test_processed_file_exist

        Description:  Test with existing processed files.

        Arguments:

        """

        mock_search.return_value = self.docid_files2
        mock_load.return_value = self.processed_files2
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_processed_file_none(self, mock_log, mock_search, mock_load,
                                 mock_recall):

        """Function:  test_processed_file_none

        Description:  Test with no processed files.

        Arguments:

        """

        mock_search.return_value = self.docid_files3
        mock_load.return_value = self.processed_files
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_file_dict_dupes(self, mock_log, mock_search, mock_load,
                             mock_recall):

        """Function:  test_file_dict_dupes

        Description:  Test with docid_files with dupe files detected.

        Arguments:

        """

        mock_search.return_value = self.docid_files4
        mock_load.return_value = self.processed_files
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_file_dict_no_dupes(self, mock_log, mock_search, mock_load,
                                mock_recall):

        """Function:  test_file_dict_no_dupes

        Description:  Test with docid_files with no dupe files detected.

        Arguments:

        """

        mock_search.return_value = self.docid_files3
        mock_load.return_value = self.processed_files
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_docid_files_multiple(self, mock_log, mock_search, mock_load,
                                  mock_recall):

        """Function:  test_docid_files_multiple

        Description:  Test with docid_files with multiple files.

        Arguments:

        """

        mock_search.return_value = self.docid_files3
        mock_load.return_value = self.processed_files
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.update_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_docid_files_single(self, mock_log, mock_search, mock_load,
                                mock_recall):

        """Function:  test_docid_files_single

        Description:  Test with docid_files with single file.

        Arguments:

        """

        mock_search.return_value = self.docid_files2
        mock_load.return_value = self.processed_files
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_docid_files_empty(self, mock_log, mock_search, mock_load,
                               mock_recall):

        """Function:  test_docid_files_empty

        Description:  Test with docid_files being empty.

        Arguments:

        """

        mock_search.return_value = self.docid_files
        mock_load.return_value = self.processed_files
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_search_dir_multiple(self, mock_log, mock_search, mock_load,
                                 mock_recall):

        """Function:  test_search_dir_multiple

        Description:  Test with multiple search directories.

        Arguments:

        """

        mock_search.return_value = self.docid_files
        mock_load.return_value = self.processed_files
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg2, mock_log))

    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_search_dir_single(self, mock_log, mock_search, mock_load,
                               mock_recall):

        """Function:  test_search_dir_single

        Description:  Test with single search directory.

        Arguments:

        """

        mock_search.return_value = self.docid_files
        mock_load.return_value = self.processed_files
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.recall_search")
    @mock.patch("pulled_search.load_processed")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_arg_m_option(self, mock_log, mock_search, mock_load, mock_recall):

        """Function:  test_arg_m_option

        Description:  Test with -m option from argument line.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_search.return_value = self.docid_files
        mock_load.return_value = self.processed_files
        mock_recall.return_value = self.failed_dict

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
