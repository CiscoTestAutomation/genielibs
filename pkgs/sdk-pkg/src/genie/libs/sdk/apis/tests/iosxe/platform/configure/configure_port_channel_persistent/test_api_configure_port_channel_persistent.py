import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_port_channel_persistent


class TestConfigurePortChannelPersistent(unittest.TestCase):

    def test_configure_port_channel_persistent(self):
        device = Mock()

        result = configure_port_channel_persistent(device, 1)

        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('port-channel 1 persistent ',)
        )