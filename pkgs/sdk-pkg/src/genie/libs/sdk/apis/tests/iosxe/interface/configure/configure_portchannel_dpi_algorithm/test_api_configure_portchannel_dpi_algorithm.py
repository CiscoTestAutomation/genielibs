import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_portchannel_dpi_algorithm,
)


class TestConfigurePortchannelDpiAlgorithm(TestCase):

    def test_configure_portchannel_dpi_algorithm(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_portchannel_dpi_algorithm(
            device,
            "tunnel-gre",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            "port-channel load-balance-hash-algo dpi algorithm tunnel-gre",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()