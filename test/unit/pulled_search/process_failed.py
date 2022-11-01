# Classification (U)

"""Program:  process_failed.py

    Description:  Unit testing of process_failed in pulled_search.py.

    Usage:
        test/unit/pulled_search/process_failed.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import pulled_search
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


def file_to_list(fname):

    """Function:  file_to_list

    Description:  Read file into a list.

    Arguments:
        (input) fname -> Name of file
        (output) filelist -> List of file entries

    """

    with open(fname) as fhdr:
        filelist = fhdr.readlines()
        filelist = [line.rstrip() for line in filelist]

    return filelist


class Mail(object):

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__
        add_2_msg
        send_mail

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.data = None

    def add_2_msg(self, data):

        """Method:  add_2_msg

        Description:  Stub method holder for Mail.add_2_msg.

        Arguments:

        """

        self.data = data

        return True

    def send_mail(self):

        """Method:  send_mail

        Description:  Stub method holder for Mail.send_mail.

        Arguments:

        """

        return True


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

        self.error_dir = "test/unit/pulled_search/tmp"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_email_no_subject
        test_email_subject
        test_write_file
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.basepath = "test/unit/pulled_search/tmp"
        self.basefile = "failed_process."
        self.fname = None
        self.args = ArgParser()
        self.cfg = CfgTest()
        self.mail = Mail()
        self.args_array = {"-t": "EmailAddr"}
        self.args_array2 = {"-t": "EmailAddr", "-s": "Subject"}
        self.failed_dict = {"/path/file1": "Error Message"}

    @mock.patch("pulled_search.gen_class.setup_mail")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_email_no_subject(self, mock_log, mock_mail):

        """Function:  test_email_no_subject

        Description:  Test with email and no subject.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.args.args_array = self.args_array2

        self.assertFalse(
            pulled_search.process_failed(
                self.args, self.cfg, mock_log, self.failed_dict))

        self.fname = gen_libs.filename_search(
            self.basepath, self.basefile, add_path=True)[0]

    @mock.patch("pulled_search.gen_class.setup_mail")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_email_subject(self, mock_log, mock_mail):

        """Function:  test_email_subject

        Description:  Test with email and subject.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.args.args_array = self.args_array

        self.assertFalse(
            pulled_search.process_failed(
                self.args, self.cfg, mock_log, self.failed_dict))

        self.fname = gen_libs.filename_search(
            self.basepath, self.basefile, add_path=True)[0]

    @mock.patch("pulled_search.gen_class.Logger")
    def test_write_file(self, mock_log):

        """Function:  test_write_file

        Description:  Test with writing to file.

        Arguments:

        """

        pulled_search.process_failed(
            self.args, self.cfg, mock_log, self.failed_dict)
        self.fname = gen_libs.filename_search(
            self.basepath, self.basefile, add_path=True)[0]

        self.assertTrue(os.path.isfile(self.fname))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        if os.path.isfile(self.fname):
            os.remove(self.fname)


if __name__ == "__main__":
    unittest.main()
