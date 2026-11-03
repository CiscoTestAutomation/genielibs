import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.execute import (
    execute_crypto_pki_server,
)


class TestExecuteCryptoPkiServer(TestCase):

    def test_execute_crypto_pki_server(self):
        device = Mock()
        device.execute.return_value = None

        result = execute_crypto_pki_server(
            device,
            "enroll",
            "server",
            "None",
            5,
        )

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "crypto pki enroll server")
        device.execute.assert_called_once_with(command)


if __name__ == "__main__":
    unittest.main()
