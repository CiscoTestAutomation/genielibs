from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cdp.configure import configure_cdp_timer

class TestConfigureCdpTimer(TestCase):

    def test_configure_cdp_timer(self):
        device = Mock()
        result = configure_cdp_timer(device, 30)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['cdp timer 30'],)
        )