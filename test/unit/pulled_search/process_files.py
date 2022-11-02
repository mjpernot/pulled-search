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
        self.processed_dir = "/dir/path/processed_dir"
        self.processed_file = "processed_file.txt"


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
        self.processed_dir = "/dir/path/processed_dir"
        self.processed_file = "processed_file.txt"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_failed_dict
        test_update_process
        test_processed_file_some
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
        self.args_array = {"-m": "/dir_path/doc_dir3"}
        self.docid_files = list()
        self.processed_files = list()
        self.failed_dict = list()

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





##############################################################################
    @unittest.skip("Skip")
    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_empty_docdir(self, mock_log):

        """Function:  test_empty_docdir

        Description:  Test with no doc directory.

        Arguments:

        """

        self.args.args_array = dict()
        self.cfg.doc_dir = []

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @unittest.skip("Skip")
    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_docdir(self, mock_log):

        """Function:  test_multiple_docdir

        Description:  Test with multiple doc directories.

        Arguments:

        """

        self.args.args_array = dict()
        self.cfg.doc_dir.append("/dir_path/doc_dir2")

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @unittest.skip("Skip")
    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_docdir(self, mock_log):

        """Function:  test_single_docdir

        Description:  Test with single doc directory.

        Arguments:

        """

        self.args.args_array = dict()

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @unittest.skip("Skip")
    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_preamble(self, mock_log):

        """Function:  test_with_preamble

        Description:  Test with pre-amble subject.

        Arguments:

        """

        self.args.args_array = self.args_array3

        mock_log.return_value = True

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @unittest.skip("Skip")
    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_no_mail(self, mock_log):

        """Function:  test_with_no_mail

        Description:  Test with no mail setup.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_log.return_value = True

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @unittest.skip("Skip")
    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_nonprocessed_files(self, mock_log):

        """Function:  test_nonprocessed_files

        Description:  Test with nonprocessed files.

        Arguments:

        """

        self.args.args_array = dict()

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @unittest.skip("Skip")
    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_no_log_files(self, mock_log):

        """Function:  test_no_log_files

        Description:  Test with no log files detected.

        Arguments:

        """

        self.args.args_array = dict()

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @unittest.skip("Skip")
    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_mail(self, mock_log):

        """Function:  test_with_mail

        Description:  Test with mail setup.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))

    @unittest.skip("Skip")
    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=[]))
    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search",
                mock.Mock(return_value=[]))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_data(self, mock_log):

        """Function:  test_with_data

        Description:  Test with successful log file check.

        Arguments:

        """

        self.args.args_array = dict()

        self.assertFalse(
            pulled_search.process_files(self.args, self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
