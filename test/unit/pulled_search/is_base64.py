# Classification (U)

"""Program:  is_base64.py

    Description:  Unit testing of is_base64 in pulled_search.py.

    Usage:
        test/unit/pulled_search/is_base64.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_with_str_data5
        test_with_str_data4
        test_with_str_data3
        test_with_str_data2
        test_with_str_data
        test_with_encoded_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.data = 'dGhpcyBpcyBhIHRlc3RhIG92ZXIgYW5kIG92ZXIxMjM0'
        self.data2 = 'this is a testa over and over'
        self.data3 = 'this is a testa over and over1'
        self.data4 = 'this is a testa over and over12'
        self.data5 = 'this is a testa over and over123'
        self.data6 = 'this is a testa over and over1234'

    def test_with_str_data5(self):

        """Function:  test_with_str_data5

        Description:  Test with string data of different lengths.

        Arguments:

        """

        self.assertFalse(pulled_search.is_base64(self.data6))

    def test_with_str_data4(self):

        """Function:  test_with_str_data4

        Description:  Test with string data of different lengths.

        Arguments:

        """

        self.assertFalse(pulled_search.is_base64(self.data5))

    def test_with_str_data3(self):

        """Function:  test_with_str_data3

        Description:  Test with string data of different lengths.

        Arguments:

        """

        self.assertFalse(pulled_search.is_base64(self.data4))

    def test_with_str_data2(self):

        """Function:  test_with_str_data2

        Description:  Test with string data of different lengths.

        Arguments:

        """

        self.assertFalse(pulled_search.is_base64(self.data3))

    def test_with_str_data(self):

        """Function:  test_with_str_data

        Description:  Test with string data of different lengths.

        Arguments:

        """

        self.assertFalse(pulled_search.is_base64(self.data2))

    def test_with_encoded_data(self):

        """Function:  test_with_encoded_data

        Description:  Test with encoded data.

        Arguments:

        """

        self.assertTrue(pulled_search.is_base64(self.data))


if __name__ == "__main__":
    unittest.main()
