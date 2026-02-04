from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cdp.configure import configure_cdp_advertise_v2
from unittest.mock import Mock


class TestConfigureCdpAdvertiseV2(TestCase):

    def test_configure_cdp_advertise_v2(self):
        self.device = Mock()
        result = configure_cdp_advertise_v2(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cdp advertise-v2'],)
        )
