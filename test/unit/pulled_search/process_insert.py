# Classification (U)

"""Program:  process_insert.py

    Description:  Unit testing of process_insert in pulled_search.py.

    Usage:
        test/unit/pulled_search/process_insert.py

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

        self.mconfig = "mongo"


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

        self.dbs = "databasename"
        self.tbl = "tablename"


class Logger(object):

    """Class:  Logger

    Description:  Class which is a representation of gen_class.Logger class.

    Methods:
        __init__
        log_info
        log_err

    """

    def __init__(self, job_name, job_log, log_type, log_format, log_time):

        """Method:  __init__

        Description:  Initialization instance of the class.

        Arguments:

        """

        self.job_name = job_name
        self.job_log = job_log
        self.log_type = log_type
        self.log_format = log_format
        self.log_time = log_time
        self.data = None

    def log_info(self, data):

        """Method:  log_info

        Description:  log_info method.

        Arguments:

        """

        self.data = data

    def log_err(self, data):

        """Method:  log_err

        Description:  log_err method.

        Arguments:

        """

        self.data = data


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_mongo_failed
        test_mongo_successful
        test_json_failure
        test_with_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args.args_array = {"-d": "/config_path"}
        self.cfg = CfgTest()
        self.cfg2 = CfgTest2()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.data_list = ['{',
                          '"docID": "weotiuer",',
                          '"command": "COMMAND",',
                          '"pubDate": "20200102-101134",',
                          '"securityEnclave": "ENCLAVE",',
                          '"asOf": "20200306 084503",',
                          '"serverName": "SERVERNAME",',
                          '"logEntries": ["line1", "line2", "line3"]',
                          '}']
        self.fname = "/dir_path/092438k234_insert.json"

    @mock.patch("pulled_search.mongo_libs.ins_doc",
                mock.Mock(return_value=(False, "mongo failure")))
    @mock.patch("pulled_search.gen_libs.load_module")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    def test_mongo_failed(self, mock_list, mock_load):

        """Function:  test_mongo_failed

        Description:  Test with failed Mongo data insertion.

        Arguments:

        """

        mock_list.return_value = self.data_list
        mock_load.return_value = self.cfg2

        self.assertEqual(pulled_search.process_insert(
            self.args, self.cfg, self.fname, self.logger), False)

    @mock.patch("pulled_search.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.load_module")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    def test_mongo_successful(self, mock_list, mock_load):

        """Function:  test_mongo_successful

        Description:  Test with successful Mongo data insertion.

        Arguments:

        """

        mock_list.return_value = self.data_list
        mock_load.return_value = self.cfg2

        self.assertEqual(pulled_search.process_insert(
            self.args, self.cfg, self.fname, self.logger), True)

    @mock.patch("pulled_search.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.json.loads", mock.Mock(return_value="String"))
    @mock.patch("pulled_search.gen_libs.file_2_list")
    def test_json_failure(self, mock_list):

        """Function:  test_json_failure

        Description:  Test with conversion to JSON failure.

        Arguments:

        """

        mock_list.return_value = self.data_list

        self.assertEqual(pulled_search.process_insert(
            self.args, self.cfg, self.fname, self.logger), False)

    @mock.patch("pulled_search.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.load_module")
    @mock.patch("pulled_search.gen_libs.file_2_list")
    def test_with_data(self, mock_list, mock_load):

        """Function:  test_with_data

        Description:  Test with successful log file check.

        Arguments:

        """

        mock_list.return_value = self.data_list
        mock_load.return_value = self.cfg2

        self.assertEqual(pulled_search.process_insert(
            self.args, self.cfg, self.fname, self.logger), True)


if __name__ == "__main__":
    unittest.main()
