import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_udld_message_time


class TestConfigureUdldMessageTime(unittest.TestCase):

    def test_configure_udld_message_time(self):
        device = Mock()

        result = configure_udld_message_time(device, '30')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('udld message time 30',)
        )