from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_no_shutdown_vlan_interface_range,
)


class TestConfigureNoShutdownVlanInterfaceRange(TestCase):

    def test_configure_no_shutdown_vlan_interface_range(self):
        device = Mock()

        result = configure_no_shutdown_vlan_interface_range(
            device,
            vlan_id_from=11,
            vlan_id_to=20,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface range vlan 11-20',
                'no shutdown',
            ]
        )
