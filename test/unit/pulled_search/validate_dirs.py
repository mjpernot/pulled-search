# Classification (U)

"""Program:  validate_dirs.py

    Description:  Unit testing of validate_dirs in pulled_search.py.

    Usage:
        test/unit/pulled_search/validate_dirs.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_archive_dir_failure
        test_multiple_failures
        test_error_dir_failure
        test_outfile_failure
        test_log_dir_failure
        test_doc_dir_failure
        test_no_failures

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
                __init__

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.doc_dir = "/dir_path/doc_dir"
                self.log_dir = "/dir_path/log_dir"
                self.outfile = "/dir_path/outfile_dir/outfile"
                self.error_dir = "/dir_path/error_dir"
                self.archive_dir = "/dir_path/archive_dir"

        self.cfg = CfgTest()
        self.dockey = "/dir_path/doc_dir"
        self.errdir = "/dir_path/error_dir"
        self.docval = "Doc_dir failure"
        self.errval = "Error_dir failure"
        self.results2 = {self.dockey: self.docval}
        self.results3 = {"/dir_path/log_dir": "Log_dir failure"}
        self.results4 = {"/dir_path/outfile_dir": "Outfile failure"}
        self.results5 = {self.errdir: self.errval}
        self.results6 = {self.dockey: self.docval, self.errdir: self.errval}
        self.results7 = {"/dir_path/archive_dir": "Archive_dir failure"}
        self.chk = (True, None)
        self.chk2 = (False, self.docval)
        self.chk3 = (False, "Log_dir failure")
        self.chk4 = (False, "Outfile failure")
        self.chk5 = (False, self.errval)
        self.chk7 = (False, "Archive_dir failure")

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_archive_dir_failure(self, mock_chk):

        """Function:  test_archive_dir_failure

        Description:  Test with failure on archive_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk, self.chk,
                                self.chk7]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results7)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_multiple_failures(self, mock_chk):

        """Function:  test_multiple_failures

        Description:  Test with multiple failures.

        Arguments:

        """

        mock_chk.side_effect = [self.chk2, self.chk, self.chk, self.chk5,
                                self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results6)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_error_dir_failure(self, mock_chk):

        """Function:  test_error_dir_failure

        Description:  Test with failure on error_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk, self.chk5,
                                self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results5)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_outfile_failure(self, mock_chk):

        """Function:  test_outfile_failure

        Description:  Test with failure on outfile check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk4, self.chk,
                                self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results4)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_log_dir_failure(self, mock_chk):

        """Function:  test_log_dir_failure

        Description:  Test with failure on log_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk3, self.chk, self.chk,
                                self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results3)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_doc_dir_failure(self, mock_chk):

        """Function:  test_doc_dir_failure

        Description:  Test with failure on doc_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk2, self.chk, self.chk, self.chk,
                                self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results2)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_no_failures(self, mock_chk):

        """Function:  test_no_failures

        Description:  Test with no failures on directory checks.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk, self.chk,
                                self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), {})


if __name__ == "__main__":
    unittest.main()
