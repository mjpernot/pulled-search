#!/usr/bin/python
# Classification (U)

"""Program:  process_json.py

    Description:  Unit testing of process_json in pulled_search.py.

    Usage:
        test/unit/pulled_search/process_json.py

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
import version

__version__ = version.__version__


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


class CfgTest2(object):

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

        self.to_addr = "Email_Addr"
        self.subj = "Email_Subject"
        self.error_dir = "/dir/path/error_dir"


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

        self.to_addr = None
        self.subj = "Email_Subject"
        self.error_dir = "/dir/path/error_dir"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_email_json
        test_rabbitmq_pass
        test_rabbitmq_failed
        test_rabbitmq_failed_mail

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.cfg = CfgTest()
        self.cfg2 = CfgTest2()
        self.mail = Mail()
        self.args_array = {"-t": "EmailAddr"}
        self.log_json = {
            "DocID": "weotiuer", "Command": "COMMAND",
            "PubDate": "20200102-101134", "SecurityEnclave": "ENCLAVE",
            "AsOf": "20200306 084503", "ServerName": "SERVERNAME",
            "LogEntries": ["line1", "line2", "line3"]}

    @mock.patch("pulled_search.gen_class.setup_mail")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_email_json(self, mock_log, mock_mail):

        """Function:  test_email_json

        Description:  Test with emailing JSON document.

        Arguments:

        """

        mock_log.return_value = True
        mock_mail.return_value = self.mail

        self.assertFalse(
            pulled_search.process_json(
                self.args, self.cfg2, mock_log, self.log_json))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.rabbitmq_class.pub_2_rmq",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_rabbitmq_pass(self, mock_log):

        """Function:  test_rabbitmq_pass

        Description:  Test with success to send to RabbitMQ.

        Arguments:

        """

        mock_log.return_value = True

        self.assertFalse(
            pulled_search.process_json(
                self.args, self.cfg, mock_log, self.log_json))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.rabbitmq_class.pub_2_rmq",
                mock.Mock(return_value=(False, "Error Message")))
    @mock.patch("pulled_search.gen_class.Logger")
    def test_rabbitmq_failed(self, mock_log):

        """Function:  test_rabbitmq_failed

        Description:  Test with failure to send to RabbitMQ.

        Arguments:

        """

        mock_log.return_value = True

        self.assertFalse(
            pulled_search.process_json(
                self.args, self.cfg, mock_log, self.log_json))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.rabbitmq_class.pub_2_rmq",
                mock.Mock(return_value=(False, "Error Message")))
    @mock.patch("pulled_search.gen_class.setup_mail")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_rabbitmq_failed_mail(self, mock_log, mock_mail):

        """Function:  test_rabbitmq_failed_mail

        Description:  Test with failure to send to RabbitMQ with mail option.

        Arguments:

        """

        mock_log.return_value = True
        mock_mail.return_value = self.mail

        self.args.args_array = self.args_array

        self.assertFalse(
            pulled_search.process_json(
                self.args, self.cfg, mock_log, self.log_json))


if __name__ == "__main__":
    unittest.main()
