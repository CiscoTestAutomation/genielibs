import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.eigrp.configure import configure_interface_eigrp_v6


class TestConfigureInterfaceEigrpV6(TestCase):

    def test_configure_interface_eigrp_v6(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_interface_eigrp_v6(device, ['TenGigabitEthernet1/0/1'], '66')

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('interface TenGigabitEthernet1/0/1', sent_commands)
        self.assertIn('ipv6 eigrp 66', sent_commands)


if __name__ == '__main__':
    unittest.main()