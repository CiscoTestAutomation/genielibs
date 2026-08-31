from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.udld.configure import (
    configure_udld_message_time,
)


class TestConfigureUdldMessageTime(TestCase):

    def test_configure_udld_message_time(self):
        device = Mock()

        result = configure_udld_message_time(device, 18)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('udld message time 18')
