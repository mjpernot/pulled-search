# Classification (U)

"""Program:  process_docid.py

    Description:  Unit testing of process_docid in pulled_search.py.

    Usage:
        test/unit/pulled_search/process_docid.py

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

        self.log_type = "access_log"
        self.log_dir = "/dir_path/log"
        self.outfile = "/dir/path/outfile"
        self.archive_log_dir = "/dir/archive_dir"
        self.command = {"intelink": "eucom"}


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_process_json_failed
        test_for_command
        test_z_option
        test_pre_centos_7
        test_exception_cmd
        test_rm_file_failed
        test_file_empty
        test_with_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.chk_args = ArgParser()
        self.cfg = CfgTest()
        self.args_array = {}
        self.args_array2 = {"-a": True}
        self.args_array3 = {"-z": True}
        self.file_log = ["Line1", "Line2", "Line3"]
        self.docid_dict = {"docid": "weotiuer", "command": "COMMAND",
                           "pubdate": "20200102-101134"}
        self.docid_dict2 = {"docid": "weotiuer", "command": "intelink",
                           "pubdate": "20200102-101134"}
        self.log_json = {
            "docID": "weotiuer", "command": "COMMAND",
            "pubDate": "20200102-101134", "securityEnclave": "ENCLAVE",
            "asOf": "20200306 084503", "serverName": "SERVERNAME",
            "logEntries": ["line1", "line2", "line3"]}
        self.log_files = ["/path/logfile1", "/path/logfile2"]

    @mock.patch("pulled_search.platform.linux_distribution",
                mock.Mock(return_value=('Centos', '7.5')))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(False)))
    @mock.patch("pulled_search.create_json", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_process_json_failed(self, mock_log, mock_list, mock_match,
                                 mock_arg):

        """Function:  test_process_json_failed

        Description:  Test with process_json failing to process.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files
        mock_arg.return_value = self.chk_args

        self.assertFalse(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.platform.linux_distribution",
                mock.Mock(return_value=('Centos', '7.5')))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.create_json", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_for_command(self, mock_log, mock_list, mock_match, mock_arg):

        """Function:  test_for_command

        Description:  Test with command mapping.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict2, mock_log))

    @mock.patch("pulled_search.platform.linux_distribution",
                mock.Mock(return_value=('Centos', '7.5')))
    @mock.patch("pulled_search.zgrep_search",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.create_json", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_z_option(self, mock_log, mock_list, mock_match):

        """Function:  test_z_option

        Description:  Test with the -z option.

        Arguments:

        """

        self.args.args_array = self.args_array3

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.platform.linux_distribution",
                mock.Mock(return_value=('Centos', '6.10')))
    @mock.patch("pulled_search.zgrep_search",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.create_json", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_pre_centos_7(self, mock_log, mock_list, mock_match):

        """Function:  test_pre_centos_7

        Description:  Test with pre-CentOS 7 OS.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.platform.linux_distribution",
                mock.Mock(return_value=('Centos', '7.5')))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.create_json", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.get_archive_files")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_archive_option(self, mock_log, mock_list, mock_match, mock_arg):

        """Function:  test_archive_option

        Description:  Test with archive option set.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.platform.linux_distribution",
                mock.Mock(return_value=('Centos', '7.5')))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.create_json", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_exception_cmd(self, mock_log, mock_list, mock_match, mock_arg):

        """Function:  test_exception_cmd

        Description:  Test with exception command passed.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.platform.linux_distribution",
                mock.Mock(return_value=('Centos', '7.5')))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.create_json", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(False, "Error Message")))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_rm_file_failed(self, mock_log, mock_list, mock_match, mock_arg):

        """Function:  test_rm_file_failed

        Description:  Test with failure to remove outfile.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.platform.linux_distribution",
                mock.Mock(return_value=('Centos', '7.5')))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_file_empty(self, mock_log, mock_list, mock_match, mock_arg):

        """Function:  test_file_empty

        Description:  Test with no log entries returned.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.platform.linux_distribution",
                mock.Mock(return_value=('Centos', '7.5')))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.create_json", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_data(self, mock_log, mock_list, mock_match, mock_arg):

        """Function:  test_with_data

        Description:  Test with successful log file check.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))


if __name__ == "__main__":
    unittest.main()
