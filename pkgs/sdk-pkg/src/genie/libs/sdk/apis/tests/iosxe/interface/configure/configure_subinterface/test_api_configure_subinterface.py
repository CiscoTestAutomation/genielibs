from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_subinterface_action,
    configure_subinterface,
)
from unittest.mock import Mock


class TestConfigureSubinterface(TestCase):

    def test_configure_subinterface(self):
        self.device = Mock()
        result = configure_subinterface(self.device, 'Te1/0/5', '301', '172.32.24.1', '255.255.255.252', 'native', 'FACTORY_VRF')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Te1/0/5.301', 'encapsulation dot1q 301 native', 'vrf forwarding FACTORY_VRF', 'ip address 172.32.24.1 255.255.255.252'],)
        )

    def test_configure_interface_subinterface_action(self):
        self.device = Mock()
        result = configure_interface_subinterface_action(
            self.device,
            'GigabitEthernet0/1',
            '10',
            'description Uplink_To_DataCenter',
        )
        self.assertIsNone(result)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/1.10', 'description Uplink_To_DataCenter'],)
        )

    def test_configure_interface_subinterface_action_without_subcommand(self):
        self.device = Mock()
        result = configure_interface_subinterface_action(self.device, 'uut', '1')
        self.assertIsNone(result)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface uut.1'],)
        )
