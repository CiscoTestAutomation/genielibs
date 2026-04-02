import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import configure_vrf_ipv6_eigrp_named_networks


class TestConfigureVrfIpv6EigrpNamedNetworks(TestCase):

    def test_configure_vrf_ipv6_eigrp_named_networks(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_vrf_ipv6_eigrp_named_networks(device, 'test', 'unicast', 200, '', 'nsf')

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('router eigrp test', sent_commands)
        self.assertIn('address-family ipv6 unicast autonomous-system 200', sent_commands)
        self.assertIn('nsf', sent_commands)


if __name__ == '__main__':
    unittest.main()