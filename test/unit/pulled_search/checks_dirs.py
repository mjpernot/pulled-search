# Classification (U)

"""Program:  checks_dirs.py

    Description:  Unit testing of checks_dirs in pulled_search.py.

    Usage:
        test/unit/pulled_search/checks_dirs.py

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


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


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
        self.monitor_dir = "/dir_path/monitor_dir"
        self.log_dir = "/dir_path/log_dir"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_i_option
        test_p_option
        test_no_options

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.name = "name@domain"
        self.args_array = {"-t": self.name}
        self.args_array2 = {"-t": self.name, "-P": True}
        self.args_array3 = {"-t": self.name, "-I": True}
        self.results = {}
        self.results2 = {"-P": True}
        self.results3 = {"-I": True}

    @mock.patch("pulled_search.mvalidate_dirs",
                mock.Mock(return_value={"-I": True}))
    def test_i_option(self):

        """Function:  test_i_option

        Description:  Test with i option in args_array.

        Arguments:

        """

        self.args.args_array = self.args_array3

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results3)

    @mock.patch("pulled_search.validate_dirs",
                mock.Mock(return_value={"-P": True}))
    def test_p_option(self):

        """Function:  test_p_option

        Description:  Test with p option in args_array.

        Arguments:

        """

        self.args.args_array = self.args_array2

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results2)

    def test_no_options(self):

        """Function:  test_no_options

        Description:  Test with no options in args_array.

        Arguments:

        """

        self.args.args_array = self.args_array

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results)


if __name__ == "__main__":
    unittest.main()
