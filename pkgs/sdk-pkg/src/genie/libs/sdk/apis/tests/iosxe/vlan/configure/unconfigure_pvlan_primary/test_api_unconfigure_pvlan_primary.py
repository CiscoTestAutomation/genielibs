import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfigure_pvlan_primary


class TestUnconfigurePvlanPrimary(unittest.TestCase):

    def test_unconfigure_pvlan_primary(self):
        device = Mock()

        result = unconfigure_pvlan_primary(device, 2, 6)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vlan 2',
                'no private-vlan primary',
                'no private-vlan association 6',
            ]
        )
