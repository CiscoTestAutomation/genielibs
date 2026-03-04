from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.clear import clear_authentication_session
from unittest.mock import Mock


class TestClearAuthenticationSession(TestCase):

    def test_clear_authentication_session(self):
        self.device = Mock()
        results_map = {
            'clear authentication sessions interface gig0/0': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_authentication_session(self.device, 'gig0/0')
        self.assertIn(
            'clear authentication sessions interface gig0/0',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)