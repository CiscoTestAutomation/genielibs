from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cdp.configure import configure_cdp_holdtime

class TestConfigureCdpHoldtime(TestCase):

    def test_configure_cdp_holdtime(self):
        device = Mock()
        result = configure_cdp_holdtime(device, 50)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['cdp holdtime 50'],)
        )