import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import configure_arp_access_list_permit_ip_host


class TestConfigureArpAccessListPermitIpHost(unittest.TestCase):

    def test_configure_arp_access_list_permit_ip_host(self):
        device = Mock()

        device.configure = Mock()

        result = configure_arp_access_list_permit_ip_host(
            device=device,
            name='allowed_acl',
            action='permit',
            ip_address='10.1.1.1',
            mac_address='0000.1111.2222',
        )

        self.assertIsNone(result)

        device.configure(['arp access-list allowed_acl', 'permit ip host 10.1.1.1 any log'])