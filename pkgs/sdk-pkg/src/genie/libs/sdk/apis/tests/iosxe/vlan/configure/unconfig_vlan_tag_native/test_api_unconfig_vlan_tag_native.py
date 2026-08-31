import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfig_vlan_tag_native


class TestUnconfigVlanTagNative(unittest.TestCase):

    def test_unconfig_vlan_tag_native(self):
        device = Mock()

        result = unconfig_vlan_tag_native(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no vlan dot1q tag native'
        )
