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
        arg_exist

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return True if arg in self.args_array else False


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
        self.command = {"intelink": "eucom"}
        self.enclave = "ENCLAVE"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_pulldate_exist
        test_pulldate_none
        test_outfile_not_exist
        test_archive_multiple_servers
        test_archive_non_gz
        test_archive_option
        test_process_json_failed
        test_for_command
        test_rm_file_failed
        test_file_empty
        test_current_data

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
        self.file_log = ["Line1", "Line2", "Line3"]
        self.docid_dict = {"docid": "09109uosdhf", "command": "COMMAND",
                           "pubdate": "20200102-101134"}
        self.docid_dict2 = {"docid": "09109uosdhf", "command": "intelink",
                            "pubdate": "20200102-101134"}
        self.docid_dict3 = {"docid": "09109uosdhf", "command": "COMMAND",
                            "pubdate": "20200102-101134",
                            "pulldate": "20230426"}
        self.log_json = {
            "docid": "09109uosdhf",
            "command": "COMMAND",
            "pubDate": "20200102-101134",
            "network": "ENCLAVE",
            "asOf": "20230306 084503",
            "servers": {"server_name": ["line1", "line2", "line3"]}}
        self.log_files = ["/path/logs/access.log1", "/path/logs/access.log2"]
        self.log_files2 = ["/path/logs/access.log1.servername.gz",
                           "/path/logs/access.log2.servername.gz"]
        self.log_files3 = ["/path/logs/access.log1.servername",
                           "/path/logs/access.log2.servername"]
        self.log_files4 = ["/path/logs/access.log1.servername.gz",
                           "/path/logs/access.log2.servername2.gz"]

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.get_archive_files")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_pulldate_exist(self, mock_log, mock_list, mock_match, mock_arg):

        """Function:  test_pulldate_exist

        Description:  Test with pulldate set to a date.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files2
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict3, mock_log))

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.get_archive_files")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_pulldate_none(self, mock_log, mock_list, mock_match, mock_arg):

        """Function:  test_pulldate_none

        Description:  Test with pulldate set to None.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files2
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.os.path.exists",
                mock.Mock(return_value=(False)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_outfile_not_exist(self, mock_log, mock_list, mock_match,
                               mock_arg):

        """Function:  test_outfile_not_exist

        Description:  Test with no outfile existing.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.get_archive_files")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_archive_multiple_servers(self, mock_log, mock_list, mock_match,
                                      mock_arg):

        """Function:  test_archive_multiple_servers

        Description:  Test with archive option with multiple server names.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files4
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.get_archive_files")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_archive_non_gz(self, mock_log, mock_list, mock_match, mock_arg):

        """Function:  test_archive_non_gz

        Description:  Test with archive option with non-gunzipped files.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_log.return_value = True
        mock_list.return_value = self.file_log
        mock_match.return_value = self.log_files3
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
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
        mock_match.return_value = self.log_files2
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(False)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
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

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
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

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
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

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_file_empty(self, mock_log, mock_match, mock_arg):

        """Function:  test_file_empty

        Description:  Test with no log entries returned.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_match.return_value = self.log_files
        mock_arg.return_value = self.chk_args

        self.assertTrue(pulled_search.process_docid(
            self.args, self.cfg, self.docid_dict, mock_log))

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.process_json", mock.Mock(return_value=(True)))
    @mock.patch("pulled_search.check_log.run_program",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.is_empty_file",
                mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.ArgParser")
    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_current_data(self, mock_log, mock_list, mock_match, mock_arg):

        """Function:  test_current_data

        Description:  Test with on server with active log files.

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
