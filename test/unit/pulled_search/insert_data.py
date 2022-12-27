# Classification (U)

"""Program:  insert_data.py

    Description:  Unit testing of insert_data in pulled_search.py.

    Usage:
        test/unit/pulled_search/insert_data.py

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

        self.mfile_regex = "*_insert.json"
        self.monitor_dir = "/dir_path/monitor_dir"
        self.merror_dir = "/dir/path/error_dir"
        self.marchive_dir = "/dir/path/archive_dir"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_with_fail_insert
        test_with_multiple_files
        test_with_single_file
        test_with_no_files
        test_with_preamble
        test_with_no_mail
        test_with_mail

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.args_array = {"-t": "name@domain"}
        self.args_array2 = {"-t": "name@domain", "-s": "Pre-amble: "}
        self.insert_list = list()
        self.insert_list2 = ["/path/file1"]
        self.insert_list3 = ["/path/file1", "/path/file2"]

    @mock.patch("pulled_search.non_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_insert", mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_fail_insert(self, mock_log, mock_search):

        """Function:  test_with_fail_insert

        Description:  Test with failed insert of file.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list2

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.non_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_insert", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_multiple_files(self, mock_log, mock_search):

        """Function:  test_with_multiple_files

        Description:  Test with multiple files detected during search.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list3

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.non_processed", mock.Mock(return_value=True))
    @mock.patch("pulled_search.cleanup_files", mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_insert", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_single_file(self, mock_log, mock_search):

        """Function:  test_with_single_file

        Description:  Test with single file detected during search.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list2

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_no_files(self, mock_log, mock_search):

        """Function:  test_with_no_files

        Description:  Test with no files detected during search.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_preamble(self, mock_log, mock_search):

        """Function:  test_with_preamble

        Description:  Test with pre-amble subject.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_log.return_value = True
        mock_search.return_value = self.insert_list

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_no_mail(self, mock_log, mock_search):

        """Function:  test_with_no_mail

        Description:  Test with no mail setup.

        Arguments:

        """

        mock_log.return_value = True
        mock_search.return_value = self.insert_list

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))

    @mock.patch("pulled_search.gen_class.setup_mail",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_mail(self, mock_log, mock_search):

        """Function:  test_with_mail

        Description:  Test with mail setup.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_search.return_value = self.insert_list

        self.assertFalse(
            pulled_search.insert_data(self.args, self.cfg, mock_log))


if __name__ == "__main__":
    unittest.main()
