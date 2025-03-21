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
import pulled_search                            # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():                                      # pylint:disable=R0903

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
        self.args_array = {}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class CfgTest():                                        # pylint:disable=R0903

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
        self.monitor_dir = "/dir_path/monitor_dir"
        self.log_dir = "/dir_path/log_dir"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_p_option_mongo2
        test_p_option_mongo
        test_f_option_mongo2
        test_f_option_mongo
        test_f_option
        test_monitor_dir_failure
        test_doc_dir_multiple_two_fail
        test_doc_dir_multiple_one_fail
        test_doc_dir_multiple
        test_doc_dir_failure
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
        self.dockey = "/dir_path/doc_dir"
        self.dockey2 = "/dir_path/doc_dir2"
        self.docval = "Doc_dir failure"
        self.docval2 = "Doc_dir failure2"
        self.monitorkey = "/dir_path/monitor_dir"
        self.monitorval = "Monitor_dir failure"
        self.mongokey = "/dir_path/mongo_dir"
        self.mongoval = "Mongo dir failure"
        self.validatekey = "/dir_path/validate_dir"
        self.validateval = "Validate dir failure"

        self.chk = (True, None)
        self.chk2 = (False, self.docval)
        self.chk2a = (False, self.docval2)
        self.chk3 = (False, self.monitorval)

        self.name = "name@domain"
        self.args_array = {"-t": self.name}
        self.args_array2 = {"-t": self.name, "-P": True}
        self.args_array3 = {"-t": self.name, "-I": True}
        self.args_array4 = {"-t": self.name, "-F": True}
        self.args_array5 = {"-t": self.name, "-P": True, "-i": True}
        self.args_array6 = {"-t": self.name, "-F": True, "-i": True}

        self.results = {}
        self.results2 = {self.dockey: self.docval}
        self.results2a = {self.dockey: self.docval, self.dockey2: self.docval2}
        self.results3 = {self.monitorkey: self.monitorval}
        self.results4 = {self.mongokey: self.mongoval}
        self.results5 = {self.validatekey: self.validateval}
        self.results5a = {self.validatekey: self.validateval,
                          self.mongokey: self.mongoval}

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    @mock.patch("pulled_search.mvalidate_dirs")
    @mock.patch("pulled_search.validate_dirs")
    def test_p_option_mongo2(self, mock_chk3, mock_mongo, mock_chk2):

        """Function:  test_p_option_mongo2

        Description:  Test with p option and mongo option.

        Arguments:

        """

        self.args.args_array = self.args_array5

        mock_mongo.return_value = self.results4
        mock_chk3.return_value = self.results5
        mock_chk2.side_effect = [self.chk, self.chk]

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results5a)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    @mock.patch("pulled_search.mvalidate_dirs")
    @mock.patch("pulled_search.validate_dirs")
    def test_p_option_mongo(self, mock_chk, mock_mongo, mock_chk2):

        """Function:  test_p_option_mongo

        Description:  Test with p option and mongo option.

        Arguments:

        """

        self.args.args_array = self.args_array5

        mock_mongo.return_value = self.results4
        mock_chk.return_value = self.results
        mock_chk2.side_effect = [self.chk, self.chk]

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results4)

    @mock.patch("pulled_search.mvalidate_dirs")
    @mock.patch("pulled_search.validate_dirs")
    def test_f_option_mongo2(self, mock_chk, mock_mongo):

        """Function:  test_f_option_mongo2

        Description:  Test with f option and mongo option.

        Arguments:

        """

        self.args.args_array = self.args_array6

        mock_mongo.return_value = self.results4
        mock_chk.return_value = self.results5

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results5a)

    @mock.patch("pulled_search.mvalidate_dirs")
    @mock.patch("pulled_search.validate_dirs", mock.Mock(return_value={}))
    def test_f_option_mongo(self, mock_mongo):

        """Function:  test_f_option_mongo

        Description:  Test with f option and mongo option.

        Arguments:

        """

        self.args.args_array = self.args_array6

        mock_mongo.return_value = self.results4

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results4)

    @mock.patch("pulled_search.validate_dirs", mock.Mock(return_value={}))
    def test_f_option(self):

        """Function:  test_f_option

        Description:  Test with f option in args_array.

        Arguments:

        """

        self.args.args_array = self.args_array4

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results)

    @mock.patch("pulled_search.mvalidate_dirs", mock.Mock(return_value={}))
    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_monitor_dir_failure(self, mock_chk):

        """Function:  test_monitor_dir_failure

        Description:  Test with failure on monitor_dir check.

        Arguments:

        """

        self.args.args_array = self.args_array3

        mock_chk.return_value = self.chk3

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results3)

    @mock.patch("pulled_search.validate_dirs", mock.Mock(return_value={}))
    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_doc_dir_multiple_two_fail(self, mock_chk):

        """Function:  test_doc_dir_multiple_two_fail

        Description:  Test with multiple directories for doc_dir, one failure.

        Arguments:

        """

        self.cfg.doc_dir.append(self.dockey2)
        self.args.args_array = self.args_array2

        mock_chk.side_effect = [self.chk2, self.chk2a]

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results2a)

    @mock.patch("pulled_search.validate_dirs", mock.Mock(return_value={}))
    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_doc_dir_multiple_one_fail(self, mock_chk):

        """Function:  test_doc_dir_multiple_one_fail

        Description:  Test with multiple directories for doc_dir, one failure.

        Arguments:

        """

        self.cfg.doc_dir.append(self.dockey2)
        self.args.args_array = self.args_array2

        mock_chk.side_effect = [self.chk2, self.chk]

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results2)

    @mock.patch("pulled_search.validate_dirs", mock.Mock(return_value={}))
    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_doc_dir_multiple(self, mock_chk):

        """Function:  test_doc_dir_multiple

        Description:  Test with multiple directories for doc_dir.

        Arguments:

        """

        self.cfg.doc_dir.append("/dir_path/doc_dir2")
        self.args.args_array = self.args_array2

        mock_chk.side_effect = [self.chk, self.chk]

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results)

    @mock.patch("pulled_search.mvalidate_dirs", mock.Mock(return_value={}))
    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_i_option(self, mock_chk):

        """Function:  test_i_option

        Description:  Test with i option in args_array.

        Arguments:

        """

        self.args.args_array = self.args_array3

        mock_chk.return_value = self.chk

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results)

    @mock.patch("pulled_search.validate_dirs", mock.Mock(return_value={}))
    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_p_option(self, mock_chk):

        """Function:  test_p_option

        Description:  Test with p option in args_array.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_chk.return_value = self.chk

        self.assertEqual(
            pulled_search.checks_dirs(self.args, self.cfg), self.results)

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
