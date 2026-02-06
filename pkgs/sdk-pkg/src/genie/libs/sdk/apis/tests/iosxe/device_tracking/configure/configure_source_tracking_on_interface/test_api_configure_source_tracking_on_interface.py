import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.device_tracking.configure import configure_source_tracking_on_interface


class TestConfigureSourceTrackingOnInterface(TestCase):

    def test_configure_source_tracking_on_interface(self):
        device = Mock()
        result = configure_source_tracking_on_interface(device, 'GigabitEthernet1/4/0/14', 'tracking')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/4/0/14', 'ip verify source tracking'],)
        )


if __name__ == '__main__':
    unittest.main()