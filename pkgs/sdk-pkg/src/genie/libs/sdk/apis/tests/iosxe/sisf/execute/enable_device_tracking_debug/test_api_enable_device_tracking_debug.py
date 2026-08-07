from unittest import TestCase
from genie.libs.sdk.apis.iosxe.sisf.execute import enable_device_tracking_debug
from unittest.mock import Mock


class TestEnableDeviceTrackingDebug(TestCase):

    def test_enable_device_tracking_debug(self):
        self.device = Mock()
        results_map = {
            'debug device-tracking': '  Device-tracking - General debugging is on',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = enable_device_tracking_debug(self.device)
        self.assertIn(
            'debug device-tracking',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
