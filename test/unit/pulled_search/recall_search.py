# Classification (U)

"""Program:  recall_search.py

    Description:  Unit testing of recall_search in pulled_search.py.

    Usage:
        test/unit/pulled_search/recall_search.py

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

        self.doc_dir = ["/dir_path/doc_dir"]


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_process_docid_passed
        test_process_docid_failed
        test_pattern_found
        test_no_pattern
        test_missing_file
        test_empty_file
        test_multiple_file_dict
        test_single_file_dict
        test_empty_file_dict

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.fname = "CMD-LEV-PULLED-20221102-0000-GEN-LEV2-090109abcdef.html"
        
        self.file_dict = {}
        self.file_dict2 = {self.fname: }
        self.file_dict3 = {self.fname: , self.fname: }
        self.results = {}

#    @mock.patch("pulled_search.process_docid", mock.Mock(return_value=True))

    @mock.patch("pulled_search.gen_class.Logger")
    def test_empty_file_dict(self, mock_log):

        """Function:  test_empty_file_dict

        Description:  Test with empty file_dict.

        Arguments:

        """

        self.assertEqual(
            pulled_search.recall_search(
                self.args, self.cfg, mock_log, self.file_dict), self.results)


if __name__ == "__main__":
    unittest.main()
