#!/usr/bin/python
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
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_failures -> Test with no failures on directory checks.

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

                self.doc_dir = "/dir_path/doc_dir"
                self.log_dir = "/dir/path/log_dir"
                self.outfile = "/dir_path/outfile_dir/outfile"
                self.error_dir = "/dir/path/error_dir"

        self.cfg = CfgTest()
        self.chk = (True, None)

    @mock.patch("pulled_search.gen_libs.chk_crt_file")
    def test_no_failures(self, mock_chk):

        """Function:  test_no_failures

        Description:  Test with no failures on directory checks.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), {})


if __name__ == "__main__":
    unittest.main()
