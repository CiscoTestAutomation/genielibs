from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import config_vlan_tag_native


class TestConfigVlanTagNative(TestCase):

    def test_config_vlan_tag_native(self):
        device = Mock()
        result = config_vlan_tag_native(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('vlan dot1q tag native')
