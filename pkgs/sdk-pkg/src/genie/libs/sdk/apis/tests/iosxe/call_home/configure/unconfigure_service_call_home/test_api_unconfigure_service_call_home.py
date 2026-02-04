from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import unconfigure_service_call_home


class TestUnconfigureServiceCallHome(TestCase):

    def test_unconfigure_service_call_home(self):
        device = Mock()
        result = unconfigure_service_call_home(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no service call-home',)
        )
