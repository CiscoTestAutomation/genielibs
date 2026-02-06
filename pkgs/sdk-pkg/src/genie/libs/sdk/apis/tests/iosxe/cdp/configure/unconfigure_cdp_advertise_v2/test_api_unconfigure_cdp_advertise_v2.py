from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cdp.configure import unconfigure_cdp_advertise_v2
from unittest.mock import Mock


class TestUnconfigureCdpAdvertiseV2(TestCase):

    def test_unconfigure_cdp_advertise_v2(self):
        self.device = Mock()
        result = unconfigure_cdp_advertise_v2(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cdp advertise-v2'],)
        )
