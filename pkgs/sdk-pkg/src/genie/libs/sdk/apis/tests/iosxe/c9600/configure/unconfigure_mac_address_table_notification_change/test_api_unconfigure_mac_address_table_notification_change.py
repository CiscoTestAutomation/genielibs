from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9600.configure import unconfigure_mac_address_table_notification_change


class TestUnconfigureMacAddressTableNotificationChange(TestCase):

    def test_unconfigure_mac_address_table_notification_change(self):
        self.device = Mock()
        result = unconfigure_mac_address_table_notification_change(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no mac-address-table notification change',)
        )
