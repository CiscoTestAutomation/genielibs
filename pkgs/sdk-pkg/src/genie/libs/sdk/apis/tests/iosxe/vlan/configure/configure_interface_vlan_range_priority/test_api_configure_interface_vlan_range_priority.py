from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_interface_vlan_range_priority,
)


class TestConfigureInterfaceVlanRangePriority(TestCase):

    def test_configure_interface_vlan_range_priority(self):
        device = Mock()

        result = configure_interface_vlan_range_priority(
            device,
            vlan_id_from=11,
            vlan_id_to=20,
            stby_value=0,
            priority=50,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface range vlan 11-20',
                'standby 0 priority 50',
            ]
        )
