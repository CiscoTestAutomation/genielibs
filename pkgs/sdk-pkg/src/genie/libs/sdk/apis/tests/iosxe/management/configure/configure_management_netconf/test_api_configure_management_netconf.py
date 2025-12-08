from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_netconf
from unittest.mock import Mock


class TestConfigureManagementNetconf(TestCase):

    def test_configure_management_netconf(self):
        self.device = Mock()
        result = configure_management_netconf(self.device, None, None, None, 'cisco.com')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['netconf-yang'],)
        )
