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
import pulled_search                            # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():                                      # pylint:disable=R0903

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
        self.args_array = {}


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


class Logger():

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
        test_json_success
        test_json_failure
        test_with_encoded_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args.args_array = {"-d": "/config_path"}
        self.cfg = CfgTest()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        base = os.getcwd()
        self.in_file = os.path.join(
            base, "test/unit/pulled_search/testfiles/test_docid.json")
        self.in_file2 = os.path.join(
            base, "test/unit/pulled_search/testfiles/test_docid2.json")
        self.in_file3 = os.path.join(
            base, "test/unit/pulled_search/testfiles/test_docid3.json")

    @mock.patch("pulled_search.parse_data", mock.Mock(return_value=False))
    def test_mongo_failed(self):

        """Function:  test_mongo_failed

        Description:  Test with failed Mongo data insertion.

        Arguments:

        """

        self.assertFalse(
            pulled_search.process_insert(
                self.args, self.cfg, self.in_file, self.logger))

    @mock.patch("pulled_search.parse_data", mock.Mock(return_value=True))
    def test_mongo_successful(self):

        """Function:  test_mongo_successful

        Description:  Test with successful Mongo data insertion.

        Arguments:

        """

        self.assertTrue(
            pulled_search.process_insert(
                self.args, self.cfg, self.in_file, self.logger))

    @mock.patch("pulled_search.parse_data", mock.Mock(return_value=True))
    def test_json_success(self):

        """Function:  test_json_success

        Description:  Test with conversion to JSON successful.

        Arguments:

        """

        self.assertTrue(
            pulled_search.process_insert(
                self.args, self.cfg, self.in_file3, self.logger))

    def test_json_failure(self):

        """Function:  test_json_failure

        Description:  Test with conversion to JSON failure.

        Arguments:

        """

        self.assertFalse(
            pulled_search.process_insert(
                self.args, self.cfg, self.in_file2, self.logger))

    @mock.patch("pulled_search.parse_data", mock.Mock(return_value=True))
    def test_with_encoded_data(self):

        """Function:  test_with_encoded_data

        Description:  Test with encoded data in the file.

        Arguments:

        """

        self.assertTrue(
            pulled_search.process_insert(
                self.args, self.cfg, self.in_file, self.logger))


if __name__ == "__main__":
    unittest.main()
