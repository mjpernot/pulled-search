#!/usr/bin/python
# Classification (U)

"""Program:  create_json.py

    Description:  Unit testing of create_json in pulled_search.py.

    Usage:
        test/unit/pulled_search/create_json.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import pulled_search
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_with_data -> Test creating JSON document.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.enclave = "ENCLAVE"

        self.cfg = CfgTest()
        self.file_log = ["line1", "line2", "line3"]
        self.docid_dict = {"docid": "weotiuer", "command": "COMMAND",
                           "postdate": "20200102-101134"}
        self.results = {"docID": "weotiuer", "command": "COMMAND",
                        "postDate": "20200102-101134",
                        "securityEnclave": "ENCLAVE",
                        "asOf": "20200306 084503", "serverName": "SERVERNAME",
                        "logEntries": ["line1", "line2", "line3"]}
        self.indate = "20200306 084503"

    @mock.patch("pulled_search.socket.gethostname",
                mock.Mock(return_value="SERVERNAME"))
    @mock.patch("pulled_search.datetime.datetime")
    def test_with_data(self, mock_date):

        """Function:  test_with_data

        Description:  Test creating JSON document.

        Arguments:

        """

        mock_date.now.return_value = "(2020, 3, 6, 13, 51, 42, 852147)"
        mock_date.strftime.return_value = self.indate

        self.assertEqual(pulled_search.create_json(self.cfg, self.docid_dict,
            self.file_log), self.results)


if __name__ == "__main__":
    unittest.main()
