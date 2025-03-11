from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_ppp_multilink
from unittest.mock import Mock


class TestConfigurePppMultilink(TestCase):

    def test_configure_ppp_multilink(self):
        self.device = Mock()
        result = configure_ppp_multilink(self.device, 'Dialer10', True, 'hostname', '10')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Dialer10', 'ppp multilink', 'ppp multilink interleave', 'ppp multilink endpoint hostname', 'ppp multilink fragment delay 10'],)
        )
