from unittest import TestCase
from genie.libs.sdk.apis.iosxe.sisf.execute import disable_device_tracking_debug
from unittest.mock import Mock


class TestDisableDeviceTrackingDebug(TestCase):

    def test_disable_device_tracking_debug(self):
        self.device = Mock()
        results_map = {
            'no debug device-tracking': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = disable_device_tracking_debug(self.device)
        self.assertIn(
            'no debug device-tracking',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
