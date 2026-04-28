import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_domain_name


class TestConfigureIpDomainName(unittest.TestCase):

    def test_configure_ip_domain_name(self):
        device = Mock()

        result = configure_ip_domain_name(device, 'test')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip domain name test',)
        )