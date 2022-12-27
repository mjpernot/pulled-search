# Classification (U)

"""Program:  zgrep_search.py

    Description:  Unit testing of zgrep_search in pulled_search.py.

    Usage:
        test/unit/pulled_search/zgrep_search.py

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


class SubProcess(object):

    """Class:  SubProcess

    Description:  Class which is a representation of the subprocess class.

    Methods:
        __init__
        wait

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the ZipFile class.

        Arguments:

        """

        pass

    def wait(self):

        """Method:  wait

        Description:  Mock representation of subprocess.wait method.

        Arguments:

        """

        pass


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_file_option
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cmd = "zgrep"
        self.filelist = ["/dir_path/file1", "/dir_path/file2"]
        self.fname = "./test/unit/pulled_search/tmp/test_zgrep_search"
        self.keyword = "KEYWORD"

    @mock.patch("pulled_search.subprocess.Popen")
    def test_file_option(self, mock_open):

        """Function:  test_file_option

        Description:  Test with file option selected.

        Arguments:

        """

        mock_open.return_value = SubProcess()

        self.assertFalse(pulled_search.zgrep_search(self.filelist,
                                                    self.keyword, self.fname))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        if os.path.isfile(self.fname):
            os.remove(self.fname)


if __name__ == "__main__":
    unittest.main()
