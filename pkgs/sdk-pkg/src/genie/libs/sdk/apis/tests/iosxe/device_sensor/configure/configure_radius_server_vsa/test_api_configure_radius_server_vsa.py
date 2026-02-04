import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.device_sensor.configure import configure_radius_server_vsa


class TestConfigureRadiusServerVsa(TestCase):

    def test_configure_radius_server_vsa(self):
        device = Mock()
        result = configure_radius_server_vsa(device, 'send', 'accounting', None, 'nas-port', 'pppoa')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('radius-server vsa send accounting nas-port protocol pppoa vsa1',)
        )


if __name__ == '__main__':
    unittest.main()