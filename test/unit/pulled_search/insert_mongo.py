# Classification (U)

"""Program:  insert_mongo.py

    Description:  Unit testing of insert_mongo in pulled_search.py.

    Usage:
        test/unit/pulled_search/insert_mongo.py

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


class Mail():

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__
        add_2_msg
        send_mail

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.data = None

    def add_2_msg(self, data):

        """Method:  add_2_msg

        Description:  Stub method holder for Mail.add_2_msg.

        Arguments:

        """

        self.data = data

        return True

    def send_mail(self):

        """Method:  send_mail

        Description:  Stub method holder for Mail.send_mail.

        Arguments:

        """

        return True


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

        self.args_array = {"-d": "/config_path"}

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

        self.mconfig = "mongo"
        self.merror_dir = "/dir/path"


class MCfgTest():                                       # pylint:disable=R0903

    """Class:  MCfgTest

    Description:  Class which is a representation of a cfg module for Mongo.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.dbs = "database_name"
        self.tbl = "table_name"


class Logger():

    """Class:  Logger

    Description:  Class which is a representation of gen_class.Logger class.

    Methods:
        __init__
        log_info
        log_err

    """

    def __init__(                                       # pylint:disable=R0913
            self, job_name, job_log, log_type, log_format, log_time):

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
        test_mongo_failed_email
        test_mongo_failed
        test_mongo_successful

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.mcfg = MCfgTest()
        self.mail = Mail()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.data = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE",
            "asOf": "20200306 084503", "entry": "data_line",
            "logTime": "log_time", "userID": "user_id", "requestMethod": "GET"}

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.mongo_libs.ins_doc",
                mock.Mock(return_value=(False, "mongo failure")))
    @mock.patch("pulled_search.gen_class.setup_mail")
    @mock.patch("pulled_search.gen_libs.load_module")
    def test_mongo_failed_email(self, mock_load, mock_mail):

        """Function:  test_mongo_failed_email

        Description:  Test with failed Mongo data insertion.

        Arguments:

        """

        self.args.args_array["-t"] = "email_address"

        mock_load.return_value = self.mcfg
        mock_mail.return_value = self.mail

        self.assertFalse(pulled_search.insert_mongo(
            self.args, self.cfg, self.logger, self.data))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.mongo_libs.ins_doc",
                mock.Mock(return_value=(False, "mongo failure")))
    @mock.patch("pulled_search.gen_libs.load_module")
    def test_mongo_failed(self, mock_load):

        """Function:  test_mongo_failed

        Description:  Test with failed Mongo data insertion.

        Arguments:

        """

        mock_load.return_value = self.mcfg

        self.assertFalse(pulled_search.insert_mongo(
            self.args, self.cfg, self.logger, self.data))

    @mock.patch("pulled_search.mongo_libs.ins_doc",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_libs.load_module")
    def test_mongo_successful(self, mock_load):

        """Function:  test_mongo_successful

        Description:  Test with successful Mongo data insertion.

        Arguments:

        """

        mock_load.return_value = self.mcfg

        self.assertTrue(pulled_search.insert_mongo(
            self.args, self.cfg, self.logger, self.data))


if __name__ == "__main__":
    unittest.main()
