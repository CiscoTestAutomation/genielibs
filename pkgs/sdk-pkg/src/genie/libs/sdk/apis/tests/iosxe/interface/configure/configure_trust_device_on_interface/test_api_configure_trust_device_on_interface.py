from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_trust_device_on_interface
from unittest.mock import Mock


class TestConfigureTrustDeviceOnInterface(TestCase):

    def test_configure_trust_device_on_interface(self):
        self.device = Mock()
        result = configure_trust_device_on_interface(self.device, 'GigabitEthernet1/0/1', 'cisco-phone')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/1', 'trust device cisco-phone'],)
        )
