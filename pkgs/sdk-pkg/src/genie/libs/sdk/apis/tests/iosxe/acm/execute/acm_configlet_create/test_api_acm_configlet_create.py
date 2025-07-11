from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm.execute import acm_configlet_create
from unittest.mock import Mock


class TestAcmConfigletCreate(TestCase):

    def test_acm_configlet_create(self):
        self.device = Mock()
        results_map = {
            'acm configlet create tftp://10.85.64.40/auto/tftp-ott-users1/ammanika/acm/configlet_merge1': '''Config file read with end:
interface Port-channel81
!
interface Port-channel82

end

Configlet tftp://10.85.64.40/auto/tftp-ott-users1/ammanika/acm/configlet_merge1 created successfully

configlet  created from tftp://10.85.64.40/auto/tftp-ott-users1/ammanika/acm/configlet_merge1''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_configlet_create(self.device, 'tftp://10.85.64.40/auto/tftp-ott-users1/ammanika/acm/configlet_merge1', None, 90)
        self.assertIn(
            'acm configlet create tftp://10.85.64.40/auto/tftp-ott-users1/ammanika/acm/configlet_merge1',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
