from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    config_ip_on_vlan,
)


class TestConfigIpOnVlan(TestCase):

    def test_config_ip_on_vlan(self):
        device = Mock()

        result = config_ip_on_vlan(
            device,
            vlan_id='101',
            ipv4_address='10.230.62.50',
            subnetmask='255.255.255.0',
            secondary=True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface vlan 101',
                'ip address 10.230.62.50 255.255.255.0 secondary',
            ]
        )
