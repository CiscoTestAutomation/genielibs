from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import config_interface_default_mtu
from unittest.mock import Mock


class TestConfigInterfaceDefaultMtu(TestCase):

    def test_config_interface_default_mtu(self):
        self.device = Mock()
        result = config_interface_default_mtu(self.device, 'Tw0/0/0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Tw0/0/0', 'default mtu'],)
        )
