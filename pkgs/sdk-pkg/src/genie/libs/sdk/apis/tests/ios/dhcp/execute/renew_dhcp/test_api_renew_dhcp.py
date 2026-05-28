from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.dhcp.execute import renew_dhcp


class TestRenewDhcp(TestCase):

    def test_renew_dhcp(self):
        device = Mock()
        renew_dhcp(device, "GigabitEthernet0/0")
        device.execute.assert_called_once_with("renew dhcp GigabitEthernet0/0")

    def test_renew_dhcp_failure(self):
        device = Mock()
        device.execute.side_effect = SubCommandFailure("cli error")
        with self.assertRaises(SubCommandFailure):
            renew_dhcp(device, "GigabitEthernet0/0")
