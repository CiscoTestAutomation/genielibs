from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.network_policy.configure import unconfigure_network_policy_profile_number

class TestUnconfigureNetworkPolicyProfileNumber(TestCase):

    def test_unconfigure_network_policy_profile_number(self):
        device = Mock()
        result = unconfigure_network_policy_profile_number(device, '1')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no network-policy profile 1'],)
        )