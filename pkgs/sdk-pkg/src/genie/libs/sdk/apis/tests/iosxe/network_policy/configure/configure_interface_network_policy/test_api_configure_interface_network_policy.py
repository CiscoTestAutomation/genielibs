from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.network_policy.configure import configure_interface_network_policy

class TestConfigureInterfaceNetworkPolicy(TestCase):

    def test_configure_interface_network_policy(self):
        device = Mock()
        result = configure_interface_network_policy(device, 'GigabitEthernet3/0/1', 1)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet3/0/1', 'network-policy 1'],)
        )