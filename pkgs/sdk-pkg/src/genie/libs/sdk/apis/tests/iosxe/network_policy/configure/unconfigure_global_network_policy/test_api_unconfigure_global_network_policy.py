from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.network_policy.configure import unconfigure_global_network_policy

class TestUnconfigureGlobalNetworkPolicy(TestCase):

    def test_unconfigure_global_network_policy(self):
        device = Mock()
        result = unconfigure_global_network_policy(device, 2)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no network-policy profile 2'],)
        )