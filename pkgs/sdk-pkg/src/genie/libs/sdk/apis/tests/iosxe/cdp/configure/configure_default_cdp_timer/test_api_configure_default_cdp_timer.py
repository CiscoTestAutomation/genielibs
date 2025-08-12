from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cdp.configure import configure_default_cdp_timer
from unittest.mock import Mock


class TestConfigureDefaultCdpTimer(TestCase):

    def test_configure_default_cdp_timer(self):
        self.device = Mock()
        result = configure_default_cdp_timer(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['default cdp timer'],)
        )
