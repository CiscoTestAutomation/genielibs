from unittest import TestCase
from genie.libs.sdk.apis.iosxe.apphosting.configure import enable_app_hosting_verification
from unittest.mock import Mock


class TestEnableAppHostingVerification(TestCase):

    def test_enable_app_hosting_verification(self):
        self.device = Mock()
        results_map = {
            'app-hosting verification enable': 'Application signature verification is enabled while using bootflash',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = enable_app_hosting_verification(self.device)
        self.assertIn(
            'app-hosting verification enable',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
