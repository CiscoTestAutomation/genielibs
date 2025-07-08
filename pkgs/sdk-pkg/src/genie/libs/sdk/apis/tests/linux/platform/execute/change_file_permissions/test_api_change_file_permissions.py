from unittest import TestCase
from genie.libs.sdk.apis.linux.platform.execute import change_file_permissions
from unittest.mock import Mock


class TestChangeFilePermissions(TestCase):

    def test_change_file_permissions(self):
        self.device = Mock()
        results_map = {
            'chmod 777 /auto/iatest/file/newfile1': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = change_file_permissions(self.device, '/auto/iatest/file/newfile1', '777')
        self.assertIn(
            'chmod 777 /auto/iatest/file/newfile1',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
