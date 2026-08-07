from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.dhcp.execute import clear_ip_dhcp_binding


class TestClearIpDhcpBinding(TestCase):

    def test_clear_ip_dhcp_binding(self):
        self.device = Mock()
        clear_ip_dhcp_binding(device=self.device)
        self.device.execute.assert_called_once_with(
            "clear ip dhcp binding *"
        )

    def test_clear_ip_dhcp_binding_failure(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            clear_ip_dhcp_binding(device=self.device)
