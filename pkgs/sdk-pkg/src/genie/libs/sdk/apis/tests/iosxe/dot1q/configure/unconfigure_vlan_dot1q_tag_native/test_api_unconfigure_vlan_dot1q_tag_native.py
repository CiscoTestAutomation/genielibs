import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dot1q.configure import unconfigure_vlan_dot1q_tag_native

class TestUnconfigureVlanDot1qTagNative(TestCase):

    def test_unconfigure_vlan_dot1q_tag_native(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Simulate enable mode

        result = unconfigure_vlan_dot1q_tag_native(device)
        expected_output = None
        self.assertEqual(result, expected_output)

        # Check that the expected command was sent
        self.assertIn(
            'no vlan dot1q tag native',
            device.configure.mock_calls[0].args[0]
        )

if __name__ == '__main__':
    unittest.main()