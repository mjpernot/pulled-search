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

        self.mongo = None
        # Regular expression to parse access log entries
        sect1 = r"(?P<ip>.*?) (?P<proxyid>.*?) (?P<userid>.*?) "
        sect2 = r"\[(?P<logTime>.*?)(?= ) (?P<timeZone>.*?)\] "
        sect3 = r"(?P<requestid>.*?) (?P<secs>.*?)/(?P<msecs>.*?) "
        sect4 = r"\"(?P<verb>.*?) HTTP/(?P<httpVer>.*?)\" (?P<status>.*?) "
        sect5 = r"(?P<length>.*?) \"(?P<referrer>.*?)\" "
        sect6 = r"\"(?P<userAgent>.*?)\" (?P<url>.*?)?$"
        self.regex = sect1 + sect2 + sect3 + sect4 + sect5 + sect6
        self.allowable = ["userid", "logTime", "verb", "status", "url"]
        self.marchive_dir = "/path/to/archive"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_url_no_transformer
        test_url_no_docid
        test_url_contains_2ndreview
        test_url_contains_ic_gov
        test_bad_status_code
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

        ip1 = "1.1.1.1 "
        proxy = "- "
        user = "CN=First Last M username,OU=People,OU=N,OU=DoD,O=U.S. Gov,C=US"
        dtg2 = " [31/Jan/2023:00:00:33 +0000] "
        reqid = "Y9hakjsdhfkjsfhksdfkhsddf 0/826818 "
        verb = '"GET /ddd/products?quey_here&callback=jQuerylfjksfh HTTP/1.1" '
        stats = "200 18331 "
        stats2 = "404 18331 "
        ref = '"https://hp.on.ic.gov/transform/20220805-1436-GEN-010109.html" '
        agt = '"Moz/5.0 Win NT 10; Win64; AWK/5.6 (KHTML Geck)Chr/1.0 Saf/5.6"'
        url = " jsk.dfh/transformer/dio/source/ProductPage?docid=09109uosdhf"
        url2 = " hp.on.ic.gov/proxy/dio/source/ProductPage?docid=09109uosdhf"
        url3 = " hp.on.ic.gov/2ndReview/source/ProductPage?docid=09109uosdhf"
        url4 = " jsk.dfh/transformer/dio/source/ProductPage?docid=09109abcdhf"
        url5 = " jsk.dfh/notcorrect/dio/source/ProductPage?docid=09109uosdhf"
        line3 = ' - - [08/Jan/2020:21:39:03 +0000] "GET / HTTP/1.1" 200 6169 '
        line4 = '"-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        line5 = '(KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"'
        dtg = "2020-03-06T08:45:03Z"

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.entry1 = ip1 + proxy + user + dtg2 + reqid + verb + stats \
            + ref + agt + url
        self.entry2 = ip1 + line3 + line4 + line5
        self.entry3 = ip1 + proxy + user + dtg2 + reqid + verb + stats2 \
            + ref + agt + url
        self.entry4 = ip1 + proxy + user + dtg2 + reqid + verb + stats \
            + ref + agt + url2
        self.entry5 = ip1 + proxy + user + dtg2 + reqid + verb + stats \
            + ref + agt + url3
        self.entry6 = ip1 + proxy + user + dtg2 + reqid + verb + stats \
            + ref + agt + url4
        self.entry7 = ip1 + proxy + user + dtg2 + reqid + verb + stats \
            + ref + agt + url5
        self.log_json = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE", "asOf": dtg,
            "servers": {"server_name": [self.entry1]}}
        self.log_json2 = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE", "asOf": dtg,
            "servers": {"server_name": [self.entry1, self.entry1]}}
        self.log_json3 = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE", "asOf": dtg,
            "servers": {"server_name": [self.entry1],
                        "server_name2": [self.entry1]}}
        self.log_json4 = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE", "asOf": dtg,
            "servers": {"server_name": [self.entry2]}}
        self.log_json5 = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE", "asOf": dtg,
            "servers": {"server_name": [self.entry3]}}
        self.log_json6 = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE", "asOf": dtg,
            "servers": {"server_name": [self.entry4]}}
        self.log_json7 = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE", "asOf": dtg,
            "servers": {"server_name": [self.entry5]}}
        self.log_json8 = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE", "asOf": dtg,
            "servers": {"server_name": [self.entry6]}}
        self.log_json9 = {
            "docid": "09109uosdhf", "command": "COMMAND",
            "pubDate": "20200102-101134", "network": "ENCLAVE", "asOf": dtg,
            "servers": {"server_name": [self.entry7]}}

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_url_no_transformer(self, mock_log):

        """Function:  test_url_no_transformer

        Description:  Test with url does not contain transformer.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(
            pulled_search.parse_data(
                self.args, self.cfg, mock_log, self.log_json9))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_url_no_docid(self, mock_log):

        """Function:  test_url_no_docid

        Description:  Test with url does not contain the right DocID.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(
            pulled_search.parse_data(
                self.args, self.cfg, mock_log, self.log_json8))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_url_contains_2ndreview(self, mock_log):

        """Function:  test_url_contains_2ndreview

        Description:  Test with url that contains 2ndReview.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(
            pulled_search.parse_data(
                self.args, self.cfg, mock_log, self.log_json7))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_url_contains_ic_gov(self, mock_log):

        """Function:  test_url_contains_ic_gov

        Description:  Test with url that contains .ic.gov.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(
            pulled_search.parse_data(
                self.args, self.cfg, mock_log, self.log_json6))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_bad_status_code(self, mock_log):

        """Function:  test_bad_status_code

        Description:  Test with bad status code.

        Arguments:

        """

        mock_log.return_value = True

        self.assertTrue(
            pulled_search.parse_data(
                self.args, self.cfg, mock_log, self.log_json5))

    @mock.patch(
        "pulled_search.gen_libs.write_file", mock.Mock(return_value=True))
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

    @mock.patch(
        "pulled_search.gen_libs.write_file", mock.Mock(return_value=True))
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

    @mock.patch(
        "pulled_search.gen_libs.write_file", mock.Mock(return_value=True))
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

    @mock.patch(
        "pulled_search.gen_libs.write_file", mock.Mock(return_value=True))
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

    @mock.patch(
        "pulled_search.gen_libs.write_file", mock.Mock(return_value=True))
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
