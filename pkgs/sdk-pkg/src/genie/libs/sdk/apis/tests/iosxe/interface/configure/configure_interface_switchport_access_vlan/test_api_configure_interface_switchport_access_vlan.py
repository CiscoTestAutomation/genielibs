from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_switchport_access_vlan
from unittest.mock import Mock


class TestConfigureInterfaceSwitchportAccessVlan(TestCase):

    def test_configure_interface_switchport_access_vlan(self):
        self.device = Mock()
        result = configure_interface_switchport_access_vlan(self.device, 'GigabitEthernet0/2/0', '10', None, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/2/0', 'switchport access vlan 10'],)
        )
