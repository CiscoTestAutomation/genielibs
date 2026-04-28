import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_domain_timeout


class TestConfigureIpDomainTimeout(unittest.TestCase):

    def test_configure_ip_domain_timeout(self):
        device = Mock()

        result = configure_ip_domain_timeout(device, '10')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip domain timeout 10',)
        )