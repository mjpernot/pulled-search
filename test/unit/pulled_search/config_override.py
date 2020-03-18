#!/usr/bin/python
# Classification (U)

"""Program:  config_override.py

    Description:  Unit testing of config_override in pulled_search.py.

    Usage:
        test/unit/pulled_search/config_override.py

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
        test_all_changes -> Test with changes to both configuration settings.
        test_monitordir_change -> Test  monitor_dir change to config settings.
        test_docdir_change -> Test doc_dir change to configuration settings.
        test_no_changes -> Test with no changes to configuration settings.

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
                self.monitor_dir = "/dir_path/monitor_dir"

        self.cfg = CfgTest()
        self.args_array = {"-t": "name@domain"}
        self.args_array2 = {"-t": "name@domain", "-m": "/new_path/doc_dir"}
        self.args_array3 = {"-t": "name@domain", "-n": "/new_path/monitor_dir"}
        self.args_array4 = {"-t": "name@domain", "-n": "/new_path/monitor_dir",
                            "-m": "/new_path/doc_dir"}
        self.results = CfgTest()
        self.results2 = self.results
        self.results2.doc_dir = "/new_path/doc_dir"} 
        self.results3 = self.results
        self.results3.monitor_dir = "/new_path/monitor_dir"}
        self.results4 = self.results
        self.results4.doc_dir = "/new_path/doc_dir"} 
        self.results4.monitor_dir = "/new_path/monitor_dir"}

    def test_all_changes(self):

        """Function:  test_all_changes

        Description:  Test with changes to both configuration settings.

        Arguments:

        """

        self.assertEqual(pulled_search.config_override(
            self.args_array4, self.cfg), self.results4)

    def test_monitordir_change(self):

        """Function:  test_monitordir_change

        Description:  Test with monitor_dir change to configuration settings.

        Arguments:

        """

        self.assertEqual(pulled_search.config_override(
            self.args_array3, self.cfg), self.results3)

    def test_docdir_change(self):

        """Function:  test_docdir_change

        Description:  Test with doc_dir change to configuration settings.

        Arguments:

        """

        self.assertEqual(pulled_search.config_override(
            self.args_array2, self.cfg), self.results2)

    def test_no_changes(self):

        """Function:  test_no_changes

        Description:  Test with no changes to configuration settings.

        Arguments:

        """

        self.assertEqual(pulled_search.config_override(
            self.args_array, self.cfg), self.results)


if __name__ == "__main__":
    unittest.main()
