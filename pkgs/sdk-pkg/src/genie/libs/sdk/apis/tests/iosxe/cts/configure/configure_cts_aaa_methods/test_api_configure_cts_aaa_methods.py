from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_aaa_methods


class TestConfigureCtsAaaMethods(TestCase):
    def test_configure_cts_aaa_methods(self):
        device = Mock()
        result = configure_cts_aaa_methods(device, 'test_ise', 'cts_test')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['aaa authentication dot1x default group test_ise', 
              'aaa authorization network cts_test group test_ise'],)
        )