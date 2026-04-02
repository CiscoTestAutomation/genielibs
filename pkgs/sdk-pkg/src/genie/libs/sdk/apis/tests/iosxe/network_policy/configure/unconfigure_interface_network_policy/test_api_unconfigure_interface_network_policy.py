from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.network_policy.configure import unconfigure_interface_network_policy

class TestUnconfigureInterfaceNetworkPolicy(TestCase):

    def test_unconfigure_interface_network_policy(self):
        device = Mock()
        result = unconfigure_interface_network_policy(device, 'GigabitEthernet3/0/1', 1)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet3/0/1', 'no network-policy 1'],)
        )