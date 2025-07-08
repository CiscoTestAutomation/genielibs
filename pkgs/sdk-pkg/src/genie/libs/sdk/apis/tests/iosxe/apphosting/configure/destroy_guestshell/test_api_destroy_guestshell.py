from unittest import TestCase
from genie.libs.sdk.apis.iosxe.apphosting.configure import destroy_guestshell
from unittest.mock import Mock


class TestDestroyGuestshell(TestCase):

    def test_destroy_guestshell(self):
        self.device = Mock()
        results_map = {
            'guestshell destroy': '% Error: The application: guestshell, does not exist',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = destroy_guestshell(self.device)
        self.assertIn(
            'guestshell destroy',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
