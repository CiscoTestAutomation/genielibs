from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import unconfigure_call_home


class TestUnconfigureCallHome(TestCase):

    def test_unconfigure_call_home(self):
        device = Mock()
        result = unconfigure_call_home(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no call-home',)
        )
