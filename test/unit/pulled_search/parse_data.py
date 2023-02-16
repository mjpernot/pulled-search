# Classification (U)

"""Program:  parse_data.py

    Description:  Unit testing of parse_data in pulled_search.py.

    Usage:
        test/unit/pulled_search/parse_data.py

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

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()


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

        sect1 = r"(?P<ip>.*?) (?P<remote_log_name>.*?) (?P<userid>.*?) "
        sect2 = r"\[(?P<date>.*?)(?= ) (?P<timezone>.*?)\] "
        sect3 = r"\"(?P<request_method>.*?) (?P<path>.*?)"
        sect4 = r"(?P<request_version> HTTP/.*)?\" (?P<status>.*?) "
        sect5 = r"(?P<length>.*?) \"(?P<referrer>.*?)\" \"(?P<user_agent>.*?)"
        sect6 = r"\"\s*(?P<end_of_line>.+)?$"

        self.regex = sect1 + sect2 + sect3 + sect4 + sect5 + sect6


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_parsing_failed
        test_partial_log_entry
        test_multiple_servers
        test_single_svr_multiple_entries
        test_single_svr_single_entry

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        ip1 = "1.1."
        ip2 = "1.1"
        line1 = ' - - [11/Nov/2016:00:00:11 +0100] "GET /icc/ HTTP/1.1" 302 '
        line2 = '- "-" "XXX XXX XXX" - 2981 '
        line3 = ' - - [08/Jan/2020:21:39:03 +0000] "GET / HTTP/1.1" 200 6169 '
        line4 = '"-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        line5 = '(KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"'

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.entry1 = ip1 + ip2 + line1 + line2 + ip1 + ip2
        self.entry2 = ip1 + ip2 + line3 + line4 + line5
        self.log_json = {
            "docid": "09109uosdhf",
            "command": "COMMAND",
            "pubDate": "20200102-101134",
            "network": "ENCLAVE",
            "asOf": "2020-03-06T08:45:03Z",
            "servers": {"server_name": [self.entry1]}}
        self.log_json2 = {
            "docid": "09109uosdhf",
            "command": "COMMAND",
            "pubDate": "20200102-101134",
            "network": "ENCLAVE",
            "asOf": "2020-03-06T08:45:03Z",
            "servers": {"server_name": [self.entry1, self.entry1]}}
        self.log_json3 = {
            "docid": "09109uosdhf",
            "command": "COMMAND",
            "pubDate": "20200102-101134",
            "network": "ENCLAVE",
            "asOf": "2020-03-06T08:45:03Z",
            "servers": {"server_name": [self.entry1],
                        "server_name2": [self.entry1]}}
        self.log_json4 = {
            "docid": "09109uosdhf",
            "command": "COMMAND",
            "pubDate": "20200102-101134",
            "network": "ENCLAVE",
            "asOf": "2020-03-06T08:45:03Z",
            "servers": {"server_name": [self.entry2]}}

    @mock.patch("pulled_search.re.match", mock.Mock(return_value=None))
    @mock.patch("pulled_search.insert_mongo", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_parsing_failed(self, mock_log):

        """Function:  test_parsing_failed

        Description:  Test with a parsing error.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(
            pulled_search.parse_data(
                self.args, self.cfg, mock_log, self.log_json))

    @mock.patch("pulled_search.insert_mongo", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_partial_log_entry(self, mock_log):

        """Function:  test_partial_log_entry

        Description:  Test with a partial log entry.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(
            pulled_search.parse_data(
                self.args, self.cfg, mock_log, self.log_json4))

    @mock.patch("pulled_search.insert_mongo", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_multiple_servers(self, mock_log):

        """Function:  test_multiple_servers

        Description:  Test with multiple servers.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(
            pulled_search.parse_data(
                self.args, self.cfg, mock_log, self.log_json3))

    @mock.patch("pulled_search.insert_mongo", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_svr_multiple_entries(self, mock_log):

        """Function:  test_single_svr_multiple_entries

        Description:  Test with single server with a multiple entries.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(
            pulled_search.parse_data(
                self.args, self.cfg, mock_log, self.log_json2))

    @mock.patch("pulled_search.insert_mongo", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_single_svr_single_entry(self, mock_log):

        """Function:  test_single_svr_single_entry

        Description:  Test with single server with a single entry.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(
            pulled_search.parse_data(
                self.args, self.cfg, mock_log, self.log_json))


if __name__ == "__main__":
    unittest.main()
