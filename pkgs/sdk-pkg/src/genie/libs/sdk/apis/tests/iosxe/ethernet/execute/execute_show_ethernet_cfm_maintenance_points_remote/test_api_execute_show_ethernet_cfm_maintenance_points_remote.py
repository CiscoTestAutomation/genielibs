from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ethernet.execute import execute_show_ethernet_cfm_maintenance_points_remote
from unittest.mock import Mock


class TestExecuteShowEthernetCfmMaintenancePointsRemote(TestCase):

    def test_execute_show_ethernet_cfm_maintenance_points_remote(self):
        self.device = Mock()
        results_map = {
            'show ethernet cfm maintenance-points remote': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_show_ethernet_cfm_maintenance_points_remote(self.device)
        self.assertIn(
            'show ethernet cfm maintenance-points remote',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
