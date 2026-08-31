from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_interface_port_channel,
)


class TestConfigureInterfacePortChannel(TestCase):

    def test_configure_interface_port_channel(self):
        device = Mock()

        result = configure_interface_port_channel(
            device,
            channel_number='5',
            mapping_number='20',
            mapping_value='30',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface port-channel 5',
                'switchport private-vlan mapping 20 30',
            ]
        )
