# Classification (U)

"""Program:  write_summary.py

    Description:  Unit testing of write_summary in pulled_search.py.

    Usage:
        test/unit/pulled_search/write_summary.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import json
import datetime
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import pulled_search
import version

__version__ = version.__version__


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

        self.processed_file = "./test/unit/pulled_search/tmp/filename"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_multiple_count2
        test_multiple_count
        test_zero_count
        test_zero_count2
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        path = "./test/unit/pulled_search/tmp"
        yearmon = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m")
        self.f_name = os.path.join(path, "docid_transfer." + yearmon)

        self.cfg = CfgTest()
        self.log_json = {
            "docid": "09109uosdhf",
            "command": "COMMAND",
            "pubDate": "20200102-101134",
            "network": "ENCLAVE",
            "asOf": "20200306 084503",
            "servers": {"server_name": []}}
        self.log_json2 = {
            "docid": "09109uosdhg",
            "command": "COMMAND",
            "pubDate": "20200102-101135",
            "network": "ENCLAVE",
            "asOf": "20200306 084504",
            "servers": {"server_name": ["line1", "line2", "line3"]}}
        self.log_json3 = {
            "docid": "09109uosdhh",
            "command": "COMMAND",
            "pubDate": "20200102-101136",
            "network": "ENCLAVE",
            "asOf": "20200306 084505",
            "servers": {
                "server_name": ["line1", "line2", "line3"],
                "server_name2": ["line4", "line5", "line6"]}}

    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_count2(self, mock_log):

        """Function:  test_multiple_count2

        Description:  Test with count from multiple servers.

        Arguments:

        """

        mock_log.return_value = True

        pulled_search.write_summary(self.cfg, mock_log, self.log_json3)

        with open(self.f_name, "r") as fhdr:
            data = fhdr.read()

        data = json.loads(data)

        self.assertEqual(data["count"], 6)


    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_count(self, mock_log):

        """Function:  test_multiple_count

        Description:  Test with count from multiple servers.

        Arguments:

        """

        mock_log.return_value = True

        pulled_search.write_summary(self.cfg, mock_log, self.log_json3)

        self.assertTrue(os.path.isfile(self.f_name))

    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_count2(self, mock_log):

        """Function:  test_single_count2

        Description:  Test with count from single server.

        Arguments:

        """

        mock_log.return_value = True

        pulled_search.write_summary(self.cfg, mock_log, self.log_json2)

        with open(self.f_name, "r") as fhdr:
            data = fhdr.read()

        data = json.loads(data)

        self.assertEqual(data["count"], 3)


    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_count(self, mock_log):

        """Function:  test_single_count

        Description:  Test with count from single server.

        Arguments:

        """

        mock_log.return_value = True

        pulled_search.write_summary(self.cfg, mock_log, self.log_json2)

        self.assertTrue(os.path.isfile(self.f_name))

    @mock.patch("pulled_search.gen_class.Logger")
    def test_zero_count(self, mock_log):

        """Function:  test_zero_count

        Description:  Test with no entries found.

        Arguments:

        """

        mock_log.return_value = True

        pulled_search.write_summary(self.cfg, mock_log, self.log_json)

        self.assertFalse(os.path.isfile(self.f_name))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        if os.path.isfile(self.f_name):
            os.remove(self.f_name)
        


if __name__ == "__main__":
    unittest.main()
