#!/usr/bin/python
# Classification (U)

"""Program:  send_2_rabbitmq.py

    Description:  Unit testing of send_2_rabbitmq in pulled_search.py.

    Usage:
        test/unit/pulled_search/send_2_rabbitmq.py

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
import collections

# Local
sys.path.append(os.getcwd())
import pulled_search
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_failed_publish -> Test with failed publish.
        test_failed_connection -> Test with failed connection.
        test_publish_msg -> Test publishing message to RabbitMQ.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class RMQTest(object):

            """Class:  RMQTest

            Description:  Class which is a representation of a RabbitMQ class.

            Methods:
                __init__ -> Initialize configuration environment.
                create_connection -> Stub holder for create_connection method.
                publish_msg -> Stub holder for publish_msg method.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the RQTest class.

                Arguments:

                """

                self.exchange = "Test_Exchange"
                self.queue_name = "Test_Queue"
                self.status = collections.namedtuple("RQ", "is_open")
                self.channel = self.status(True)
                self.conn_status = True
                self.err_msg = ""
                self.pub_status = True

            def create_connection(self):

                """Method:  create_connection

                Description:  Stub holder for create_connection method.

                Arguments:

                """

                return self.conn_status, self.err_msg

            def publish_msg(self, msg):

                """Method:  publish_msg

                Description:  Stub holder for publish_msg method.

                Arguments:
                    (input) msg -> Message body.

                """

                return self.pub_status

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

                self.user = "USERNAME"
                self.pswd = "PSWD"
                self.host = "HOSTNAME"
                self.port = 1111
                self.exchange_name = "EXCHANGE_NAME"
                self.exchange_type = "EXCHANGE_TYPE"
                self.x_durable = True
                self.q_durable = True
                self.auto_delete = True
                self.queue = "QUEUE_NAME"
                self.r_key = "RKEY_NAME"

        self.cfg = CfgTest()
        self.rmq = RMQTest()
        self.log_json = {"key": "value"}

    @mock.patch("pulled_search.create_rmq")
    def test_failed_publish(self, mock_rmq):

        """Function:  test_failed_publish

        Description:  Test with failed publish.

        Arguments:

        """

        self.rmq.pub_status = False
        mock_rmq.return_value = self.rmq

        self.assertEqual(pulled_search.send_2_rabbitmq(
            self.cfg, self.log_json), False)

    @mock.patch("pulled_search.create_rmq")
    def test_failed_connection(self, mock_rmq):

        """Function:  test_failed_connection

        Description:  Test with failed connection.

        Arguments:

        """

        self.rmq.conn_status = False
        mock_rmq.return_value = self.rmq

        self.assertEqual(pulled_search.send_2_rabbitmq(
            self.cfg, self.log_json), False)

    @mock.patch("pulled_search.create_rmq")
    def test_publish_msg(self, mock_rmq):

        """Function:  test_publish_msg

        Description:  Test publishing message to RabbitMQ.

        Arguments:

        """

        mock_rmq.return_value = self.rmq

        self.assertEqual(pulled_search.send_2_rabbitmq(
            self.cfg, self.log_json), True)


if __name__ == "__main__":
    unittest.main()
