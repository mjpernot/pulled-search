#!/usr/bin/python
# Classification (U)

"""Program:  setup_mail.py

    Description:  Unit testing of setup_mail in pulled_search.py.

    Usage:
        test/unit/pulled_search/setup_mail.py

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
        test_subject_arg -> Test with passing subject line.
        test_t_option -> Test with -t option set.
        test_s_option -> Test with -s option set.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args_array = {"-t": "name@domain"}
        self.args_array2 = {"-t": "name@domain", "-s": "subject_line"}
        self.to = "name@domain"
        self.subj = "subject_line"
        self.subj2 = "pass_subject_line"

    def test_subject_arg(self):

        """Function:  test_subject_arg

        Description:  Test with passing subject line.

        Arguments:

        """

        mail = pulled_search.setup_mail(self.args_array, subj=self.subj2)

        self.assertEqual((mail.to, mail.subj), (self.to, self.subj2))

    def test_s_option(self):

        """Function:  test_s_option

        Description:  Test with -s option set.

        Arguments:

        """

        mail = pulled_search.setup_mail(self.args_array2)

        self.assertEqual((mail.to, mail.subj), (self.to, self.subj))

    def test_t_option(self):

        """Function:  test_t_option

        Description:  Test with -t option set.

        Arguments:

        """

        mail = pulled_search.setup_mail(self.args_array)

        self.assertEqual((mail.to, mail.subj), (self.to, None))


if __name__ == "__main__":
    unittest.main()
