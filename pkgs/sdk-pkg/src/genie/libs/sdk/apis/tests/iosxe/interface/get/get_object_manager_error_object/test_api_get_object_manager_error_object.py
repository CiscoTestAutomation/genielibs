from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.get import get_object_manager_error_object
from unittest.mock import Mock


class TestGetObjectManagerErrorObject(TestCase):

    def test_get_object_manager_error_object(self):
        self.device = Mock()
        results_map = {
            'show platform software object-manager switch 1 FP active error-object': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = get_object_manager_error_object(self.device, '1')
        self.assertIn(
            'show platform software object-manager switch 1 FP active error-object',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
