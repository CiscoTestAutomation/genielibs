from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_mab_request_attribute_2_passwd
from unittest.mock import Mock


class TestUnconfigureMabRequestAttribute2Passwd(TestCase):

    def test_unconfigure_mab_request_attribute_2_passwd(self):
        self.device = Mock()
        result = unconfigure_mab_request_attribute_2_passwd(self.device, ']hc[ZbOgC[X[_JV_cbCgIUbSAGK', '6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no mab request format attribute 2 6 ]hc[ZbOgC[X[_JV_cbCgIUbSAGK',)
        )
