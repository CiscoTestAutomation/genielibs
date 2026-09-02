from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_interface_vlan_priority,
)


class TestConfigureInterfaceVlanPriority(TestCase):

    def test_configure_interface_vlan_priority(self):
        device = Mock()

        result = configure_interface_vlan_priority(
            device,
            vlan_id=11,
            priority=200,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface vlan 11',
                'standby 11 priority 200',
            ]
        )
