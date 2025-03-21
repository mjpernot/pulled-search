# Classification (U)

"""Program:  mvalidate_dirs.py

    Description:  Unit testing of mvalidate_dirs in pulled_search.py.

    Usage:
        test/unit/pulled_search/mvalidate_dirs.py

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

        self.merror_dir = "/dir_path/error_dir"
        self.marchive_dir = "/dir_path/archive_dir"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_archive_dir_failure
        test_multiple_failures
        test_error_dir_failure
        test_no_failures

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.errorkey = "/dir_path/error_dir"
        self.errorval = "Error_dir failure"
        self.archivekey = "/dir_path/archive_dir"
        self.archiveval = "Archive_dir failure"

        self.chk = (True, None)
        self.chk5 = (False, self.errorval)
        self.chk7 = (False, self.archiveval)

        self.results = {}
        self.results5 = {self.errorkey: self.errorval}
        self.results6 = {self.errorkey: self.errorval,
                         self.archivekey: self.archiveval}
        self.results7 = {self.archivekey: self.archiveval}

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_archive_dir_failure(self, mock_chk):

        """Function:  test_archive_dir_failure

        Description:  Test with failure on archive_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk7]

        self.assertEqual(pulled_search.mvalidate_dirs(self.cfg), self.results7)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_multiple_failures(self, mock_chk):

        """Function:  test_multiple_failures

        Description:  Test with multiple failures.

        Arguments:

        """

        mock_chk.side_effect = [self.chk5, self.chk7]

        self.assertEqual(pulled_search.mvalidate_dirs(self.cfg), self.results6)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_error_dir_failure(self, mock_chk):

        """Function:  test_error_dir_failure

        Description:  Test with failure on error_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk5, self.chk]

        self.assertEqual(pulled_search.mvalidate_dirs(self.cfg), self.results5)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_no_failures(self, mock_chk):

        """Function:  test_no_failures

        Description:  Test with no failures on directory checks.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk]

        self.assertEqual(pulled_search.mvalidate_dirs(self.cfg), self.results)


if __name__ == "__main__":
    unittest.main()
