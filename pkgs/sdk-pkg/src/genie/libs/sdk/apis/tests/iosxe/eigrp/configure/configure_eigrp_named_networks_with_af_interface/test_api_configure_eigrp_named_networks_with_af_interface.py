import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import (
    configure_eigrp_named_networks_with_af_interface
)


class TestConfigureEigrpNamedNetworksWithAfInterface(TestCase):

    def test_configure_eigrp_named_networks_with_af_interface(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_eigrp_named_networks_with_af_interface(
            device,
            'EIGRP_NAME3',               # eigrp_name
            300,                         # as_number
            ['10.0.0.0'],                # networks
            '255.255.255.0',             # netmask
            '10.0.0.1',                  # router_id
            'ipv4',                      # address_family
            '',                          # vrf
            'unicast',                   # unicast_multicast
            'TwoGigabitEthernet0/0/1',   # af_interface
            False,                       # shutdown
            True,                        # bfd
            False                        # split_horizon
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('router eigrp EIGRP_NAME3', sent_commands)
        self.assertIn('address-family ipv4 unicast autonomous-system 300', sent_commands)
        self.assertIn('network 10.0.0.0 255.255.255.0', sent_commands)
        self.assertIn('eigrp router-id 10.0.0.1', sent_commands)
        self.assertIn('af-interface TwoGigabitEthernet0/0/1', sent_commands)
        self.assertIn('bfd', sent_commands)
        self.assertIn('passive-interface', sent_commands)
        self.assertIn('no split-horizon', sent_commands)
        self.assertIn('no shutdown', sent_commands)
        self.assertIn('exit-af-interface', sent_commands)


if __name__ == '__main__':
    unittest.main()