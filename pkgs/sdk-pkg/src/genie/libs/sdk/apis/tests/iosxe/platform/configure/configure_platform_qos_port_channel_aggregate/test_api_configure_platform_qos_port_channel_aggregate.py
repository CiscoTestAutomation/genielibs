import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_platform_qos_port_channel_aggregate


class TestConfigurePlatformQosPortChannelAggregate(unittest.TestCase):

    def test_configure_platform_qos_port_channel_aggregate(self):
        device = Mock()

        result = configure_platform_qos_port_channel_aggregate(device, '3')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('platform qos port-channel-aggregate 3',)
        )