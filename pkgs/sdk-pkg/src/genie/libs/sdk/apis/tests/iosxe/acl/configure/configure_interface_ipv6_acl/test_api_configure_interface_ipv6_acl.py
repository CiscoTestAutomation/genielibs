from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_interface_ipv6_acl


class TestConfigureInterfaceIpv6Acl(TestCase):

    def test_configure_interface_ipv6_acl(self):
      self.device = Mock()
      configure_interface_ipv6_acl(self.device, 'Te1/0/5', 'MULTICAST_GROUP', 'FE04::10')
      self.assertEqual(
          self.device.configure.mock_calls[0].args,
          ('interface Te1/0/5\nipv6 access-list MULTICAST_GROUP\npermit ipv6 any host FE04::10',)
      )

