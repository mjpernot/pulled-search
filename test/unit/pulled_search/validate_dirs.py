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

        self.doc_dir = ["/dir_path/doc_dir"]
        self.log_dir = "/dir_path/log_dir"
        self.outfile = "/dir_path/outfile_dir/outfile"
        self.error_dir = "/dir_path/error_dir"
        self.archive_log_dir = "/dir_path/archive_log_dir"
        self.processed_dir = "/dir_path/processed_dir"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_process_dir_fail
        test_doc_dir_multiple_two_fail
        test_doc_dir_multiple_one_fail
        test_doc_dir_multiple
        test_archive_log_dir_failure
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

        self.cfg = CfgTest()
        self.dockey = "/dir_path/doc_dir"
        self.dockey2 = "/dir_path/doc_dir2"
        self.errdir = "/dir_path/error_dir"
        self.docval = "Doc_dir failure"
        self.docval2 = "Doc_dir failure2"
        self.errval = "Error_dir failure"
        self.results2 = {self.dockey: self.docval}
        self.results2a = {self.dockey: self.docval, self.dockey2: self.docval2}
        self.results3 = {"/dir_path/log_dir": "Log_dir failure"}
        self.results4 = {"/dir_path/outfile_dir": "Outfile failure"}
        self.results5 = {self.errdir: self.errval}
        self.results6 = {self.dockey: self.docval, self.errdir: self.errval}
        self.results7 = {"/dir_path/archive_log_dir": "Archive_dir failure"}
        self.results8 = {"/dir_path/processed_dir": "Processed_dir failure"}
        self.chk = (True, None)
        self.chk2 = (False, self.docval)
        self.chk2a = (False, self.docval2)
        self.chk3 = (False, "Log_dir failure")
        self.chk4 = (False, "Outfile failure")
        self.chk5 = (False, self.errval)
        self.chk7 = (False, "Archive_dir failure")
        self.chk8 = (False, "Processed_dir failure")

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_process_dir_fail(self, mock_chk):

        """Function:  test_process_dir_fail

        Description:  Test with failure on processed_dir directory.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk, self.chk,
                                self.chk, self.chk8]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results8)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_doc_dir_multiple_two_fail(self, mock_chk):

        """Function:  test_doc_dir_multiple_two_fail

        Description:  Test with multiple directories for doc_dir, one failure.

        Arguments:

        """

        self.cfg.doc_dir.append(self.dockey2)

        mock_chk.side_effect = [self.chk2, self.chk2a, self.chk, self.chk,
                                self.chk, self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results2a)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_doc_dir_multiple_one_fail(self, mock_chk):

        """Function:  test_doc_dir_multiple_one_fail

        Description:  Test with multiple directories for doc_dir, one failure.

        Arguments:

        """

        self.cfg.doc_dir.append(self.dockey2)

        mock_chk.side_effect = [self.chk2, self.chk, self.chk, self.chk,
                                self.chk, self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results2)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_doc_dir_multiple(self, mock_chk):

        """Function:  test_doc_dir_multiple

        Description:  Test with multiple directories for doc_dir.

        Arguments:

        """

        self.cfg.doc_dir.append("/dir_path/doc_dir2")

        mock_chk.side_effect = [self.chk, self.chk, self.chk, self.chk,
                                self.chk, self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), {})

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_archive_log_dir_failure(self, mock_chk):

        """Function:  test_archive_log_dir_failure

        Description:  Test with failure on archive_log_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk7, self.chk,
                                self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results7)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_multiple_failures(self, mock_chk):

        """Function:  test_multiple_failures

        Description:  Test with multiple failures.

        Arguments:

        """

        mock_chk.side_effect = [self.chk2, self.chk, self.chk, self.chk,
                                self.chk5, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results6)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_error_dir_failure(self, mock_chk):

        """Function:  test_error_dir_failure

        Description:  Test with failure on error_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk, self.chk,
                                self.chk5, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results5)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_outfile_failure(self, mock_chk):

        """Function:  test_outfile_failure

        Description:  Test with failure on outfile check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk, self.chk4,
                                self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results4)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_log_dir_failure(self, mock_chk):

        """Function:  test_log_dir_failure

        Description:  Test with failure on log_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk3, self.chk, self.chk,
                                self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results3)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_doc_dir_failure(self, mock_chk):

        """Function:  test_doc_dir_failure

        Description:  Test with failure on doc_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk2, self.chk, self.chk, self.chk,
                                self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results2)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_no_failures(self, mock_chk):

        """Function:  test_no_failures

        Description:  Test with no failures on directory checks.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk, self.chk,
                                self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), {})


if __name__ == "__main__":
    unittest.main()
