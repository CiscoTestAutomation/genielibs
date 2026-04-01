import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    unconfigure_evpn_evi_replication_type
)


class TestUnconfigureEvpnEviReplicationType(TestCase):

    def test_unconfigure_evpn_evi_replication_type(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_evpn_evi_replication_type(
            device,
            '10',
            'vlan-based',
            'ingress'
        )

        self.assertEqual(result, None)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]
        self.assertIn('l2vpn evpn instance 10 vlan-based', sent_commands)
        self.assertIn('no replication-type ingress', sent_commands)


if __name__ == '__main__':
    unittest.main()