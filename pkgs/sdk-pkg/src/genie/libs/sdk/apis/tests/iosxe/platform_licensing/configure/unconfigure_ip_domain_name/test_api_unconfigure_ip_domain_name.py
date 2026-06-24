import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_ip_domain_name


class TestUnconfigureIpDomainName(unittest.TestCase):

    def test_unconfigure_ip_domain_name(self):
        device = Mock()

        result = unconfigure_ip_domain_name(
            device,
            'cisco.com'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip domain name cisco.com',)
        )