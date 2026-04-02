from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ip_prefix_list


class TestConfigureIpPrefixList(TestCase):

    def test_configure_ip_prefix_list(self):
        device = Mock()
        result = configure_ip_prefix_list(
            device,
            'test',
            1,
            '1.1.1.1',
            32
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip prefix-list test seq 1 permit 1.1.1.1/32',)
        )