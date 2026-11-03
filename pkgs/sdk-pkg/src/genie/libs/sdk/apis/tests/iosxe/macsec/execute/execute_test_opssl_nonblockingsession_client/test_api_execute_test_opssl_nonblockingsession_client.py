import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.execute import (
    execute_test_opssl_nonblockingsession_client,
)


class TestExecuteTestOpsslNonblockingsessionClient(TestCase):

    def test_execute_test_opssl_nonblockingsession_client(self):
        device = Mock()
        device.execute.return_value = None

        result = execute_test_opssl_nonblockingsession_client(
            device,
            "tls1.2",
            "192.168.1.1",
            "9001",
            "1",
            "10",
            "2048",
            "0",
            "client",
            "client",
        )

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "test opssl nonblockingsession client tls1.2 192.168.1.1 9001 1 10 "
            "2048 0 client client",
        )
        device.execute.assert_called_once_with(command)


if __name__ == "__main__":
    unittest.main()
