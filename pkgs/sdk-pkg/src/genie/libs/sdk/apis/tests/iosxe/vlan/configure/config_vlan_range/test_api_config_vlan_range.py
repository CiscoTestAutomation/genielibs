from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import config_vlan_range


class TestConfigVlanRange(TestCase):

    def test_config_vlan_range(self):
        device = Mock()
        result = config_vlan_range(device, 2, 513, 300)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ['vlan 2-513', 'no shutdown'],
            timeout=300,
        )
