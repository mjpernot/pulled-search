# Classification (U)

"""Program:  rm_file.py

    Description:  Unit testing of rm_file in pulled_search.py.

    Usage:
        test/unit/pulled_search/rm_file.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_file_exist
        test_file_not_exist
        test_file_rm_error

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.ofile = "/path/filelog"

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_file_exist(self, mock_log):

        """Function:  test_file_exist

        Description:  Test with file exist and removed.

        Arguments:

        """

        mock_log.return_value = True

        self.assertFalse(pulled_search.rm_file(self.ofile, mock_log))

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=False))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_file_not_exist(self, mock_log):

        """Function:  test_file_not_exist

        Description:  Test with file not existing.

        Arguments:

        """

        mock_log.return_value = True

        self.assertFalse(pulled_search.rm_file(self.ofile, mock_log))

    @mock.patch("pulled_search.os.path.exists", mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_libs.rm_file",
                mock.Mock(return_value=(False, "Remove file error")))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_file_rm_error(self, mock_log):

        """Function:  test_file_rm_error

        Description:  Test with file exist and removed with errors

        Arguments:

        """

        mock_log.return_value = True

        self.assertFalse(pulled_search.rm_file(self.ofile, mock_log))


if __name__ == "__main__":
    unittest.main()
