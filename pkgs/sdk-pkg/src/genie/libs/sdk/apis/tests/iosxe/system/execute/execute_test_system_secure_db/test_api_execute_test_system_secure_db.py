from unittest import TestCase
from genie.libs.sdk.apis.iosxe.system.execute import execute_test_system_secure_db
from unittest.mock import Mock


class TestExecuteTestSystemSecureDb(TestCase):

    def test_execute_test_system_secure_db(self):
        self.device = Mock()
        results_map = {
            'test system secure db': """=============================================================
          ACTIVE INSECURE CONFIGURATION DATABASE
=============================================================
Generated: Active Configuration Analysis
Total Active Insecure Commands: 0
Database Type: Active (Current State)
Scan Status: Complete
Next Update: No pending updates
Database State: Stable
=============================================================

=============================================================
                    DATABASE SUMMARY
=============================================================
Total Active Entries Processed: 0
Queue Status: Preserved (read-only traversal)
Memory Status: Allocated and stable
Database Integrity: Verified

=============================================================
                 SECURITY RECOMMENDATIONS
=============================================================
1. IMMEDIATE ACTION REQUIRED:
   - Review all 0 insecure configurations above
   - Follow remediation steps for each entry
   - Prioritize HIGH severity configurations

2. ONGOING MONITORING:
   - Monitor active configuration changes
   - Implement automated security scanning
   - Regular security configuration audits

3. COMPLIANCE REQUIREMENTS:
   - Document all remediation actions
   - Maintain security configuration baseline
   - Schedule periodic security reviews
=============================================================
display_insecure_config_summary: Successfully displayed active database with 0 entries
display_insecure_config_summary: Active insecure configuration database walk completed""",
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_test_system_secure_db(self.device)
        self.assertIn(
            'test system secure db',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
