#!/usr/bin/python
# Classification (U)

"""Program:  create_rmq.py

    Description:  Unit testing of create_rmq in pulled_search.py.

    Usage:
        test/unit/pulled_search/create_rmq.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_create_instance -> Test creating RabbitMQ Instance.

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

    @mock.patch("pulled_search.rabbitmq_class.RabbitMQPub")
    def test_create_instance(self, mock_rmq):

        """Function:  test_create_instance

        Description:  Test creating RabbitMQ Instance.

        Arguments:

        """

        mock_rmq.return_value = "RabbitMQ_Instance"

        self.assertEqual(pulled_search.create_rmq(
            self.cfg, self.cfg.queue, self.cfg.r_key), "RabbitMQ_Instance")


if __name__ == "__main__":
    unittest.main()
