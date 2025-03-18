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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import pulled_search                            # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class Mail():

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


class ArgParser():

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val
        arg_exist

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

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return arg in self.args_array


class CfgTest2():

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

        self.to_addr = None
        self.subj = "Email_Subject"
        self.error_dir = "/dir/path/error_dir"


class Smtplib():

    """Class:  SubProcess

    Description:  Class which is a representation of the smtplib class.

    Methods:
        __init__
        sendmail
        quit

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the subprocess class.

        Arguments:

        """

        self.frm = None
        self.toaddr = None
        self.data = None

    def sendmail(self, frm, toaddr, data):

        """Method:  sendmail

        Description:  Mock representation of sendmail method.

        Arguments:
            frm
            toaddr
            func

        """

        self.frm = frm
        self.toaddr = toaddr
        self.data = data

    def quit(self):

        """Method:  quit

        Description:  Mock representation of quit method.

        Arguments:

        """

        pass


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_email_body
        test_email_summary
        test_mongo_failed
        test_mongo
        test_email
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
        self.args_array2 = {"-i": True}
        self.args_array3 = {"-e": True}
        self.args_array4 = {"-r": True}
        self.args_array5 = {"-r": True, "-t": True}
        self.args_array6 = {"-e": True, "-b": True}
        self.args_array7 = {"-e": True, "-g": True}
        self.log_json = {
            "docid": "09109uosdhf",
            "command": "COMMAND",
            "pubDate": "20200102-101134",
            "network": "ENCLAVE",
            "asOf": "20200306 084503",
            "servers": {"server_name": ["line1", "line2", "line3"]}}
        self.log_json2 = {
            "docid": "09109uosdhf",
            "command": "COMMAND",
            "pubDate": "20200102-101134",
            "network": "ENCLAVE",
            "asOf": "20200306 084503",
            "servers": {"server_name": ["line1", "line3"]}}

    @mock.patch("pulled_search.filter_data")
    @mock.patch("pulled_search.gen_class.setup_mail")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_email_body(self, mock_log, mock_mail, mock_filter):

        """Function:  test_email_body

        Description:  Test with emailing document within email body.

        Arguments:

        """

        self.args.args_array = self.args_array7

        mock_log.return_value = True
        mock_mail.return_value = self.mail
        mock_filter.return_value = self.log_json2

        self.assertTrue(
            pulled_search.process_json(
                self.args, self.cfg2, mock_log, self.log_json))

    @mock.patch("pulled_search.write_summary", mock.Mock(return_value=True))
    @mock.patch(
        "pulled_search.socket.gethostname", mock.Mock(return_value="host"))
    @mock.patch(
        "pulled_search.getpass.getuser", mock.Mock(return_value="user"))
    @mock.patch("pulled_search.filter_data")
    @mock.patch("pulled_search.smtplib.SMTP")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_email_summary(self, mock_log, mock_mail, mock_filter):

        """Function:  test_email_summary

        Description:  Test with emailing document and creating summary.

        Arguments:

        """

        self.args.args_array = self.args_array6

        mock_log.return_value = True
        mock_mail.return_value = Smtplib()
        mock_filter.return_value = self.log_json2

        self.assertTrue(
            pulled_search.process_json(
                self.args, self.cfg2, mock_log, self.log_json))

    @mock.patch("pulled_search.filter_data")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_no_option(self, mock_log, mock_filter):

        """Function:  test_no_option

        Description:  Test with no option selected.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_log.return_value = True
        mock_filter.return_value = self.log_json2

        self.assertFalse(
            pulled_search.process_json(
                self.args, self.cfg2, mock_log, self.log_json))

    @mock.patch("pulled_search.parse_data", mock.Mock(return_value=False))
    @mock.patch("pulled_search.filter_data")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_mongo_failed(self, mock_log, mock_filter):

        """Function:  test_mongo_failed

        Description:  Test with sending document to Mongo, but fails.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_log.return_value = True
        mock_filter.return_value = self.log_json2

        self.assertFalse(
            pulled_search.process_json(
                self.args, self.cfg2, mock_log, self.log_json))

    @mock.patch("pulled_search.parse_data", mock.Mock(return_value=True))
    @mock.patch("pulled_search.filter_data")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_mongo(self, mock_log, mock_filter):

        """Function:  test_mongo

        Description:  Test with sending document to Mongo.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_log.return_value = True
        mock_filter.return_value = self.log_json2

        self.assertTrue(
            pulled_search.process_json(
                self.args, self.cfg2, mock_log, self.log_json))

    @mock.patch(
        "pulled_search.socket.gethostname", mock.Mock(return_value="host"))
    @mock.patch(
        "pulled_search.getpass.getuser", mock.Mock(return_value="user"))
    @mock.patch("pulled_search.filter_data")
    @mock.patch("pulled_search.smtplib.SMTP")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_email(self, mock_log, mock_mail, mock_filter):

        """Function:  test_email

        Description:  Test with emailing document.

        Arguments:

        """

        self.args.args_array = self.args_array3

        mock_log.return_value = True
        mock_mail.return_value = Smtplib()
        mock_filter.return_value = self.log_json2

        self.assertTrue(
            pulled_search.process_json(
                self.args, self.cfg2, mock_log, self.log_json))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.rabbitmq_class.pub_2_rmq",
                mock.Mock(return_value=(True, None)))
    @mock.patch("pulled_search.filter_data")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_rabbitmq_pass(self, mock_log, mock_filter):

        """Function:  test_rabbitmq_pass

        Description:  Test with success to send to RabbitMQ.

        Arguments:

        """

        self.args.args_array = self.args_array4

        mock_log.return_value = True
        mock_filter.return_value = self.log_json2

        self.assertTrue(
            pulled_search.process_json(
                self.args, self.cfg, mock_log, self.log_json))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.rabbitmq_class.pub_2_rmq",
                mock.Mock(return_value=(False, "Error Message")))
    @mock.patch("pulled_search.filter_data")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_rabbitmq_failed(self, mock_log, mock_filter):

        """Function:  test_rabbitmq_failed

        Description:  Test with failure to send to RabbitMQ.

        Arguments:

        """

        self.args.args_array = self.args_array4

        mock_log.return_value = True
        mock_filter.return_value = self.log_json2

        self.assertFalse(
            pulled_search.process_json(
                self.args, self.cfg, mock_log, self.log_json))

    @mock.patch("pulled_search.gen_libs.write_file",
                mock.Mock(return_value=True))
    @mock.patch("pulled_search.rabbitmq_class.pub_2_rmq",
                mock.Mock(return_value=(False, "Error Message")))
    @mock.patch("pulled_search.filter_data")
    @mock.patch("pulled_search.gen_class.setup_mail")
    @mock.patch("pulled_search.gen_class.Logger")
    def test_rabbitmq_failed_mail(self, mock_log, mock_mail, mock_filter):

        """Function:  test_rabbitmq_failed_mail

        Description:  Test with failure to send to RabbitMQ with mail option.

        Arguments:

        """

        self.args.args_array = self.args_array5

        mock_log.return_value = True
        mock_mail.return_value = self.mail
        mock_filter.return_value = self.log_json2

        self.assertFalse(
            pulled_search.process_json(
                self.args, self.cfg, mock_log, self.log_json))


if __name__ == "__main__":
    unittest.main()
