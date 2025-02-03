from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import show_platform_software_mcu_snapshot_detail_request
from unittest.mock import Mock


class TestShowPlatformSoftwareMcuSnapshotDetailRequest(TestCase):

    def test_show_platform_software_mcu_snapshot_detail_request(self):
        self.device = Mock()
        results_map = {
            'show platform software mcu switch 1 R0 snapshot_detail request': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = show_platform_software_mcu_snapshot_detail_request(self.device, '1', 'R0')
        self.assertIn(
            'show platform software mcu switch 1 R0 snapshot_detail request',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
