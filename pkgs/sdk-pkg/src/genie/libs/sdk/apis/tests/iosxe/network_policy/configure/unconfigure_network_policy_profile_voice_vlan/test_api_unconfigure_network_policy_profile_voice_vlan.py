from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.network_policy.configure import unconfigure_network_policy_profile_voice_vlan

class TestUnconfigureNetworkPolicyProfileVoiceVlan(TestCase):

    def test_unconfigure_network_policy_profile_voice_vlan(self):
        device = Mock()
        result = unconfigure_network_policy_profile_voice_vlan(device, 2, 10, True, 3, 13)
        print(device.configure.mock_calls)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'network-policy profile 2',
                'no voice vlan 10',
                'no voice-signaling vlan',
                'no voice-signaling vlan 10 cos 3',
                'no voice-signaling vlan 10 dscp 13',
            ],)
        )