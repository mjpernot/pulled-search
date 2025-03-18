# Classification (U)

"""Program:  search_docid.py

    Description:  Unit testing of search_docid in pulled_search.py.

    Usage:
        test/unit/pulled_search/search_docid.py

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


class CfgTest():

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

        self.doc_dir = ["/dir_path/doc_dir"]
        self.pattern = "JAC.pull.subtype.*.SECURITY RECALL"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_process_docid_passed
        test_process_docid_failed

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.docid = "090109abcdef"
        self.results = {}
        self.results2 = {self.docid: "Failed the process_docid process"}
        self.docid_dict = {"command": "CMD",
                           "puddate": "20230102",
                           "docid": self.docid}

    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_process_docid_passed(self, mock_log):

        """Function:  test_process_docid_passed

        Description:  Test with the process_docid passing.

        Arguments:

        """

        self.assertEqual(
            pulled_search.search_docid(
                self.args, self.cfg, self.docid_dict, mock_log), self.results)

    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_process_docid_failed(self, mock_log):

        """Function:  test_process_docid_failed

        Description:  Test with the process_docid failing.

        Arguments:

        """

        self.assertEqual(
            pulled_search.search_docid(
                self.args, self.cfg, self.docid_dict, mock_log), self.results2)


if __name__ == "__main__":
    unittest.main()
