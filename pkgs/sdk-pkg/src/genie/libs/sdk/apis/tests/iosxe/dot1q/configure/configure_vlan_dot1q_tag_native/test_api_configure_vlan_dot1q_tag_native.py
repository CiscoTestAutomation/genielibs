import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dot1q.configure import configure_vlan_dot1q_tag_native

class TestConfigureVlanDot1qTagNative(TestCase):

    def test_configure_vlan_dot1q_tag_native(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assuming device is in enable state
        
        result = configure_vlan_dot1q_tag_native(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Fix: Assert the exact command sent
        self.assertIn(
            'vlan dot1q tag native',
            device.configure.mock_calls[0].args[0]
        )

if __name__ == '__main__':
    unittest.main()