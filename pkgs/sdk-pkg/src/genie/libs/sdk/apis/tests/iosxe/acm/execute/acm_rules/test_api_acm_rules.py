from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm.execute import acm_rules
from unittest.mock import Mock


class TestAcmRules(TestCase):

    def test_acm_rules(self):
        self.device = Mock()
        results_map = {
            'acm rules tftp://10.85.64.40/auto/tftp-ott-users1/ammanika/acm/acm_rule1': '''Rules file read:

match mode mdt-subscription-mode command no update-policy
 action skip
match mode mdt-subscription-mode command no stream
 action skip
match mode mdt-subscription-mode command no filter
 action skip
match mode mdt-subscription-mode command no encoding
 action skip
match mode rogue-rule command no match
 action skip
match mode rogue-rule command no classify malicious
 action skip
match mode main-cpu command no main-cpu
 action post-apply
match mode flowmon command no record wireless
 action skip
match mode configure command no wireless country
 action skip
end

Config Rules created successfully from tftp://10.85.64.40/auto/tftp-ott-users1/ammanika/acm/acm_rule1''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_rules(self.device, 'tftp://10.85.64.40/auto/tftp-ott-users1/ammanika/acm/acm_rule1', None, 90)
        self.assertIn(
            'acm rules tftp://10.85.64.40/auto/tftp-ott-users1/ammanika/acm/acm_rule1',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
