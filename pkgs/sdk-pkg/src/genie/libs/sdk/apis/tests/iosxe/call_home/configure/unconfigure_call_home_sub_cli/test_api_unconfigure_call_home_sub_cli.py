from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import unconfigure_call_home_sub_cli


class TestUnconfigureCallHomeSubCli(TestCase):

    def test_unconfigure_call_home_sub_cli(self):
        device = Mock()
        result = unconfigure_call_home_sub_cli(device, 'rate-limit')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home',  'no rate-limit'],)
        )
