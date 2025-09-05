from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_pvlan_for_output_service_policy
from unittest.mock import Mock


class TestConfigurePvlanForOutputServicePolicy(TestCase):

    def test_configure_pvlan_for_output_service_policy(self):
        self.device = Mock()
        result = configure_pvlan_for_output_service_policy(self.device, 'GigabitEthernet3/0/26', '1,2,10', '10', '2', 'pm-marking-verify', '2p6q')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet3/0/26', 'switchport private-vlan trunk allowed vlan 1,2,10', 'switchport private-vlan mapping trunk 10 2', 'switchport mode private-vlan trunk promiscuous', 'service-policy output pm-marking-verify', 'service-policy type queueing output 2p6q'],)
        )
