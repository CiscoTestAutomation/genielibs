from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.execute import execute_show_debug
from unittest.mock import Mock


class TestExecuteShowDebug(TestCase):

    def test_execute_show_debug(self):
        self.device = Mock()
        results_map = {
            'show debug': '''IOSXE Conditional Debug Configs:

Conditional Debug Global State: Stop


IOSXE Packet Tracing Configs: 





Packet Infra debugs:

Ip Address                                               Port
------------------------------------------------------|----------''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_show_debug(self.device)
        self.assertIn(
            'show debug',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = results_map['show debug']
        self.assertEqual(result, expected_output)
