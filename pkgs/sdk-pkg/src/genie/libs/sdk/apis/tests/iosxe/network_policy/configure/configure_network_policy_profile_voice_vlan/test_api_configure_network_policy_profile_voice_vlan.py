from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.network_policy.configure import configure_network_policy_profile_voice_vlan

class TestConfigureNetworkPolicyProfileVoiceVlan(TestCase):

    def test_configure_network_policy_profile_voice_vlan(self):
        device = Mock()
        result = configure_network_policy_profile_voice_vlan(device, 2, 10, 3, 13, True)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'network-policy profile 2',
                'voice vlan 10',
                'voice vlan 10 cos 3',
                'voice vlan 10 dscp 13',
                'voice-signaling vlan 10',
                'voice-signaling vlan 10 cos 3',
                'voice-signaling vlan 10 dscp 13',
            ],)
        )