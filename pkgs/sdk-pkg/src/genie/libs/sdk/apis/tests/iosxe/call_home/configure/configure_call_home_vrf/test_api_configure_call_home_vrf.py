from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_vrf


class TestConfigureCallHomeVrf(TestCase):

    def test_configure_call_home_vrf(self):
        device = Mock()
        result = configure_call_home_vrf(device, 'vrf1')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'vrf vrf1'],)
        )
