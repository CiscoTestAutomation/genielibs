from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.udld.configure import (
    unconfigure_udld_message_time,
)


class TestUnconfigureUdldMessageTime(TestCase):

    def test_unconfigure_udld_message_time(self):
        device = Mock()

        result = unconfigure_udld_message_time(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no udld message time')
