import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    unconfigure_evpn_l2_profile_bd_association
)


class TestUnconfigureEvpnL2ProfileBdAssociation(TestCase):

    def test_unconfigure_evpn_l2_profile_bd_association(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = unconfigure_evpn_l2_profile_bd_association(
            device,
            10,          # bridge_domain
            'evpn_va1'   # profile
        )

        self.assertEqual(result, None)

        device.configure.assert_called_once()
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('bridge-domain 10', sent_commands)
        self.assertIn('no member evpn-instance profile evpn_va1', sent_commands)


if __name__ == '__main__':
    unittest.main()