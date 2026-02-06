import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_service_dhcp


class TestConfigureServiceDhcp(TestCase):

    def test_configure_service_dhcp(self):
        device = Mock()
        result = configure_service_dhcp(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('service dhcp',)
        )


if __name__ == '__main__':
    unittest.main()