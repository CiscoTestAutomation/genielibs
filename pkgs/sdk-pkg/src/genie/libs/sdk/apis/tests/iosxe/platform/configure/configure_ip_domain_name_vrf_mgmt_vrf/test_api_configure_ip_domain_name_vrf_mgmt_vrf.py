import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_domain_name_vrf_mgmt_vrf


class TestConfigureIpDomainNameVrfMgmtVrf(unittest.TestCase):

    def test_configure_ip_domain_name_vrf_mgmt_vrf(self):
        device = Mock()

        result = configure_ip_domain_name_vrf_mgmt_vrf(device, 'test')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip domain name vrf mgmt-vrf test',)
        )