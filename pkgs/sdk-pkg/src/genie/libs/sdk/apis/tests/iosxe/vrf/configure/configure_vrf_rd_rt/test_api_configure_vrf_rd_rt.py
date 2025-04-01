from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_vrf_rd_rt
from unittest.mock import Mock


class TestConfigureVrfRdRt(TestCase):

    def test_configure_vrf_rd_rt(self):
        self.device = Mock()
        result = configure_vrf_rd_rt(self.device, 'red', '200:1', 'both')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip vrf red', 'rd 200:1', 'route-target both 200:1'],)
        )
