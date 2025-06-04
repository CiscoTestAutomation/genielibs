from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_exclude_ip_dhcp


class TestUnconfigureExcludeIpDhcp(TestCase):

  def test_unconfigure_exclude_ip_dhcp(self):
    self.device = Mock()
    unconfigure_exclude_ip_dhcp(self.device, '1.1.1.1', '1.1.1.2', 'Mgmt-vrf')
    self.assertEqual(
        self.device.configure.mock_calls[0].args,
        (['no ip dhcp excluded-address vrf Mgmt-vrf 1.1.1.1 1.1.1.2'],)
    )
