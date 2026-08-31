import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfig_vlan_range


class TestUnconfigVlanRange(unittest.TestCase):

    def test_unconfig_vlan_range(self):
        device = Mock()

        result = unconfig_vlan_range(device, 2, 513, 300)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'no vlan 2-513',
            ],
            timeout=300,
        )
