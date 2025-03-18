# Classification (U)

"""Program:  load_processed.py

    Description:  Unit testing of load_processed in pulled_search.py.

    Usage:
        test/unit/pulled_search/load_processed.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

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
        test_missing_file
        test_no_file_name
        test_single_file_name
        test_multiple_file_names

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        basepath = "test/unit/pulled_search/testfiles"
        self.fname = os.path.join(basepath, "test_load_processed.txt")
        self.fname2 = os.path.join(basepath, "test_load_processed2.txt")
        self.fname3 = os.path.join(basepath, "test_load_processed3.txt")
        self.fname4 = os.path.join(basepath, "test_load_processed0.txt")
        self.results = ["docid1", "docid2"]
        self.results2 = ["docid1"]
        self.results3 = []

    def test_missing_file(self):

        """Function:  test_missing_file

        Description:  Test with missing file.

        Arguments:

        """

        self.assertEqual(
            pulled_search.load_processed(self.fname4), self.results3)

    def test_no_file_name(self):

        """Function:  test_no_file_name

        Description:  Test with no file names in file.

        Arguments:

        """

        self.assertEqual(
            pulled_search.load_processed(self.fname3), self.results3)

    def test_single_file_name(self):

        """Function:  test_single_file_name

        Description:  Test with single file names in file.

        Arguments:

        """

        self.assertEqual(
            pulled_search.load_processed(self.fname2), self.results2)

    def test_multiple_file_names(self):

        """Function:  test_multiple_file_names

        Description:  Test with multiple file names in file.

        Arguments:

        """

        self.assertEqual(
            pulled_search.load_processed(self.fname), self.results)


if __name__ == "__main__":
    unittest.main()
