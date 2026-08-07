import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_portchannel_dpi_algorithm,
)


class TestUnconfigurePortchannelDpiAlgorithm(TestCase):

    def test_unconfigure_portchannel_dpi_algorithm(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_portchannel_dpi_algorithm(
            device,
            "tunnel-gre",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "no port-channel load-balance-hash-algo dpi algorithm tunnel-gre",
        )


if __name__ == "__main__":
    unittest.main()