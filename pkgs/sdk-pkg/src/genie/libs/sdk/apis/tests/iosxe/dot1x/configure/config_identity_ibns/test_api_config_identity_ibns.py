import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dot1x.configure import config_identity_ibns

class TestConfigIdentityIbns(TestCase):

    def test_config_identity_ibns(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Simulate device in enable mode

        result = config_identity_ibns(device, None, 'HundredGigE1/0/23', True, 'auto', None, 'both')
        expected_output = None
        self.assertEqual(result, expected_output)

        # Collect commands sent to device.configure
        sent_commands = device.configure.mock_calls[0].args[0]
        
        expected_commands = [
            'interface HundredGigE1/0/23',
            'switchport',
            'switchport mode access',
            'authentication periodic',
            'mab',
            'access-session port-control auto',
            'dot1x pae both'
        ]
        # Assert all expected commands are present in sent_commands
        for command in expected_commands:
            self.assertIn(command, sent_commands)

if __name__ == '__main__':
    unittest.main()