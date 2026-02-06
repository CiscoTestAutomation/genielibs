from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9600.configure import configure_mac_address_table_notification_change

class TestConfigureMacAddressTableNotificationChange(TestCase):

    def test_configure_mac_address_table_notification_change(self):
        device = Mock()
        result = configure_mac_address_table_notification_change(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('mac-address-table notification change',)
        )