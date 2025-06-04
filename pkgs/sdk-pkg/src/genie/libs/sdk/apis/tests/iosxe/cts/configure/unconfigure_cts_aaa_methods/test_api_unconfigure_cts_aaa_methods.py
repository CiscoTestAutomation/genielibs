from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_aaa_methods
from unittest.mock import Mock


class TestUnconfigureCtsAaaMethods(TestCase):

    def test_unconfigure_cts_aaa_methods(self):
        self.device = Mock()
        result = unconfigure_cts_aaa_methods(self.device, 'test_ise', 'cts_test')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no aaa authentication dot1x default group test_ise', 'no aaa authorization network cts_test group test_ise'],)
        )
