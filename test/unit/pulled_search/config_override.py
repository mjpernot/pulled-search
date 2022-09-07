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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_all_changes
        test_monitordir_change
        test_docdir_change
        test_no_changes

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.name = "name@domain"
        self.docdir = "/new_path/doc_dir"
        self.monitordir = "/new_path/monitor_dir"
        self.args_array = {"-t": self.name}
        self.args_array2 = {"-t": self.name, "-m": self.docdir}
        self.args_array3 = {"-t": self.name, "-n": self.monitordir}
        self.args_array4 = {"-t": self.name, "-n": self.monitordir,
                            "-m": self.docdir}
        self.results = "/dir_path/doc_dir"
        self.results2 = "/dir_path/monitor_dir"
        self.results3 = self.docdir
        self.results4 = self.monitordir

    def test_all_changes(self):

        """Function:  test_all_changes

        Description:  Test with changes to both configuration settings.

        Arguments:

        """

        self.args.args_array = self.args_array4
        cfg = pulled_search.config_override(self.args, self.cfg)

        self.assertEqual(
            (cfg.doc_dir, cfg.monitor_dir), (self.results3, self.results4))

    def test_monitordir_change(self):

        """Function:  test_monitordir_change

        Description:  Test with monitor_dir change to configuration settings.

        Arguments:

        """

        self.args.args_array = self.args_array3
        cfg = pulled_search.config_override(self.args, self.cfg)

        self.assertEqual(
            (cfg.doc_dir, cfg.monitor_dir), (self.results, self.results4))

    def test_docdir_change(self):

        """Function:  test_docdir_change

        Description:  Test with doc_dir change to configuration settings.

        Arguments:

        """

        self.args.args_array = self.args_array2
        cfg = pulled_search.config_override(self.args, self.cfg)

        self.assertEqual(
            (cfg.doc_dir, cfg.monitor_dir), (self.results3, self.results2))

    def test_no_changes(self):

        """Function:  test_no_changes

        Description:  Test with no changes to configuration settings.

        Arguments:

        """

        self.args.args_array = self.args_array
        cfg = pulled_search.config_override(self.args, self.cfg)
        self.assertEqual(
            (cfg.doc_dir, cfg.monitor_dir), (self.results, self.results2))


if __name__ == "__main__":
    unittest.main()
