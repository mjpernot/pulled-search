#!/usr/bin/python
# Classification (U)

"""Program:  non_processed.py

    Description:  Unit testing of non_processed in pulled_search.py.

    Usage:
        test/unit/pulled_search/non_processed.py

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


class Mail(object):

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__ -> Class initialization.
        add_2_msg -> Stub method holder for Mail.add_2_msg.
        send_mail -> Stub method holder for Mail.send_mail.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        pass

    def add_2_msg(self, data):

        """Method:  add_2_msg

        Description:  Stub method holder for Mail.add_2_msg.

        Arguments:
            (input) data -> Message line to add to email body.

        """

        return True

    def send_mail(self):

        """Method:  send_mail

        Description:  Stub method holder for Mail.send_mail.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_data -> Test with no data in file list.
        test_no_mail -> Test no mail instance argument.
        test_with_data -> Test data in file list.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.mail = Mail()
        self.docid_files = ["/tmp/a", "/tmp/b"]
        self.docid_files2 = []
        self.error_dir = "/dir/error_dir"

    def test_no_data(self):

        """Function:  test_no_data

        Description:  Test with no data in file list.

        Arguments:

        """

        self.assertFalse(pulled_search.non_processed(
            self.docid_files2, self.error_dir, mock_log, self.mail))

    @mock.patch("pulled_search.gen_libs.mv_file2",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_no_mail(self, mock_log):

        """Function:  test_no_mail

        Description:  Test no mail instance argument.

        Arguments:

        """

        mock_log.return_value = "Log Instance"

        self.assertFalse(pulled_search.non_processed(
            self.docid_files, self.error_dir, mock_log))

    @mock.patch("pulled_search.gen_libs.mv_file2",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_with_data(self, mock_log):

        """Function:  test_with_data

        Description:  Test data in file list.

        Arguments:

        """

        mock_log.return_value = "Log Instance"

        self.assertFalse(pulled_search.non_processed(
            self.docid_files, self.error_dir, mock_log, self.mail))


if __name__ == "__main__":
    unittest.main()
