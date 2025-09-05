from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_pvlan_for_input_service_policy
from unittest.mock import Mock


class TestConfigurePvlanForInputServicePolicy(TestCase):

    def test_configure_pvlan_for_input_service_policy(self):
        self.device = Mock()
        result = configure_pvlan_for_input_service_policy(self.device, 'GigabitEthernet3/0/25', 1, '2,10', '10 2', '10 2', 'trunk', 'policer-cos3')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet3/0/25', 'switchport private-vlan trunk native vlan 1', 'switchport private-vlan trunk allowed vlan 2,10', 'switchport private-vlan association trunk 10 2', 'switchport private-vlan mapping trunk 10 2', 'switchport mode private-vlan trunk', 'service-policy input policer-cos3'],)
        )
