from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cdp.configure import configure_interface_cdp_enable
from unittest.mock import Mock


class TestConfigureInterfaceCdpEnable(TestCase):

    def test_configure_interface_cdp_enable(self):
        self.device = Mock()
        result = configure_interface_cdp_enable(self.device, 'GigabitEthernet0/1/7')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/1/7', 'cdp enable'],)
        )
