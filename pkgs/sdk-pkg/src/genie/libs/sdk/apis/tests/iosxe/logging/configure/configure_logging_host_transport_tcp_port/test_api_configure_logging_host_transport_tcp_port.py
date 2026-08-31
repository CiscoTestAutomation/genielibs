import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.logging.configure import (
    configure_logging_host_transport_tcp_port,
)


class TestConfigureLoggingHostTransportTcpPort(TestCase):

    def test_configure_logging_host_transport_tcp_port(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_logging_host_transport_tcp_port(
            device,
            "1.1.1.1",
            "1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "logging host 1.1.1.1 transport tcp port 1",
        )


if __name__ == "__main__":
    unittest.main()
