#!/usr/bin/python
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
        test_with_data -> Test with successful log file check.

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

                self.log_type = "access_log"
                self.log_dir = "/dir_path/log"
                self.outfile = "/dir/path/outfile"

        self.cfg = CfgTest()
        self.data_list = ['{',
                          '"docid": "weotiuer"',
                          '"command": "COMMAND"',
                          '"postdate": "20200102-101134"',
                          '}']
        self.file_log = ["Line1", "Line2", "Line3"]
        self.fname = "/dir_path/092438k234_docid.json"
        self.docid_dict = {"docid": "weotiuer", "command": "COMMAND",
                           "postdate": "20200102-101134"}
        self.log_json = {"docID": "weotiuer", "command": "COMMAND",
                         "postDate": "20200102-101134",
                         "securityEnclave": "ENCLAVE",
                         "asOf": "20200306 084503", "serverName": "SERVERNAME",
                         "logEntries": ["line1", "line2", "line3"]}

    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_data(self, mock_log):

        """Function:  test_with_data

        Description:  Test with successful log file check.

        Arguments:

        """

        mock_log.return_value = True

        self.assertEqual(pulled_search.process_docid(self.cfg, self.fname,
            mock_log), True)


if __name__ == "__main__":
    unittest.main()
