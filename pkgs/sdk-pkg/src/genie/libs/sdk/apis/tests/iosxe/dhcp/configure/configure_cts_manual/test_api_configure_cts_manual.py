import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_cts_manual


class TestConfigureCtsManual(TestCase):

    def test_configure_cts_manual(self):
        device = Mock()
        result = configure_cts_manual(device, 'FiftyGigE1/0/1', 'yes', '1234', None, 'yes')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface FiftyGigE1/0/1', 'cts manual', 'policy static sgt 1234', 'no propagate sgt'],)
        )


if __name__ == '__main__':
    unittest.main()