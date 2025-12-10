from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_group_radius_interface
from unittest.mock import Mock


class TestConfigureAaaGroupRadiusInterface(TestCase):

    def test_configure_aaa_group_radius_interface(self):
        self.device = Mock()
        result = configure_aaa_group_radius_interface(self.device, 'ISE', 'vlan100', 'ip', None, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['aaa group server radius ISE', 'ip radius source-interface vlan100'],)
        )
