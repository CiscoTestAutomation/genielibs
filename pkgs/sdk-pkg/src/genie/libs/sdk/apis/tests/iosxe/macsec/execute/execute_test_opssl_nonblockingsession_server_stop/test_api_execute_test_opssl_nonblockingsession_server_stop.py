import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.execute import (
    execute_test_opssl_nonblockingsession_server_stop,
)


class TestExecuteTestOpsslNonblockingsessionServerStop(TestCase):

    def test_execute_test_opssl_nonblockingsession_server_stop(self):
        device = Mock()
        device.execute.return_value = None

        result = execute_test_opssl_nonblockingsession_server_stop(
            device,
            "server",
            "tls1.2",
            "stop",
        )

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "test opssl nonblockingsession server tls1.2 stop",
        )
        device.execute.assert_called_once_with(command)


if __name__ == "__main__":
    unittest.main()
