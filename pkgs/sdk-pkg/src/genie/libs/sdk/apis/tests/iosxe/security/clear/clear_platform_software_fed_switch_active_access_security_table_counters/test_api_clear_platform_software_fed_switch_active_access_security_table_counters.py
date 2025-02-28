from unittest import TestCase
from genie.libs.sdk.apis.iosxe.security.clear import clear_platform_software_fed_switch_active_access_security_table_counters
from unittest.mock import Mock


class TestClearPlatformSoftwareFedSwitchActiveAccessSecurityTableCounters(TestCase):

    def test_clear_platform_software_fed_switch_active_access_security_table_counters(self):
        self.device = Mock()
        results_map = {
            'clear platform software fed switch standby access-security table counters': '(unlicensed)',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_platform_software_fed_switch_active_access_security_table_counters(self.device, 'standby')
        self.assertIn(
            'clear platform software fed switch standby access-security table counters',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
