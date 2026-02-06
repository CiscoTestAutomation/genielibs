from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import clear_cts_pac_all
from unittest.mock import Mock


class TestClearCtsPacAll(TestCase):

    def test_clear_cts_pac_all(self):
        self.device = Mock()
        results_map = {
        'clear cts pac all': """This may disrupt connectivity on your CTS links.
        Are you sure you want to delete all PACs? [confirm]""",
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_cts_pac_all(self.device)
        self.assertIn(
            'clear cts pac all',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
