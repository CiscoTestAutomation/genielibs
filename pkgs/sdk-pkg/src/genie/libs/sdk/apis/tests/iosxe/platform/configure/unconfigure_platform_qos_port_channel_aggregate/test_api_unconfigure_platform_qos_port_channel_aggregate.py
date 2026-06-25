import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import (
    unconfigure_platform_qos_port_channel_aggregate
)


class TestUnconfigurePlatformQosPortChannelAggregate(unittest.TestCase):

    def test_unconfigure_platform_qos_port_channel_aggregate(self):
        device = Mock()

        result = unconfigure_platform_qos_port_channel_aggregate(device, '3')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no platform qos port-channel-aggregate 3',)
        )