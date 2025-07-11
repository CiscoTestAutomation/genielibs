from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm.execute import acm_rules_match_mode
from unittest.mock import Mock


class TestAcmRulesMatchMode(TestCase):

    def test_acm_rules_match_mode(self):
        self.device = Mock()
        result = acm_rules_match_mode(self.device, 'mdt-subscription-mode', 'no update-policy', True, False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['match mode mdt-subscription-mode command no update-policy', 'action skip'],)
        )
