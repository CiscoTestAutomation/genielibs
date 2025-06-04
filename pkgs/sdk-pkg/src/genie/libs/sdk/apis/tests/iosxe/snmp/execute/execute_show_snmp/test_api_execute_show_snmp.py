from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.snmp.execute import execute_show_snmp

class TestExecuteShowSnmp(TestCase):

    def test_execute_show_snmp(self):
        self.device = Mock()
        results_map = {
            'show snmp engineID': 'Local SNMP engineID: 800000090300000C29F12216\n'
                                  'Remote Engine ID          IP-addr    Port',
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = execute_show_snmp(self.device, 'engineID')
        self.assertIn(
            'show snmp engineID',
            self.device.execute.call_args_list[0][0][0]
        )
        expected_output = ('Local SNMP engineID: 800000090300000C29F12216\n'
                           'Remote Engine ID          IP-addr    Port')
        self.assertEqual(result, expected_output)
