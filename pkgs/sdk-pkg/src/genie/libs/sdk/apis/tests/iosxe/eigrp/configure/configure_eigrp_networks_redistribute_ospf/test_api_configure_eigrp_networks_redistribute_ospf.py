
import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import (
    configure_eigrp_networks_redistribute_ospf
)


class TestConfigureEigrpNetworksRedistributeOspf(TestCase):

    def test_configure_eigrp_networks_redistribute_ospf(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_eigrp_networks_redistribute_ospf(
            device,
            '101',        # eigrp_as
            '101.0.0.0',   # network
            None,         # netmask
            '1000',       # bandwidth
            '100',        # delay
            '255',        # reliability
            '1',          # load
            '1500'        # mtu
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('router eigrp 101', sent_commands)
        self.assertIn('network 101.0.0.0', sent_commands)
        self.assertIn(
            'redistribute ospf 101 metric 1000 100 255 1 1500',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()