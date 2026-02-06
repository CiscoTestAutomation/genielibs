from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_service_call_home


class TestConfigureServiceCallHome(TestCase):
    
    def test_configure_service_call_home(self):
        device = Mock()
        result = configure_service_call_home(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
        device.configure.mock_calls[0].args,
        ('service call-home',)
        )     
