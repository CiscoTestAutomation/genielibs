import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vpdn.configure import (
    unconfigure_vpdn_l2tp_attribute_physical_channel_id,
)


class TestUnconfigureVpdnL2tpAttributePhysicalChannelId(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_unconfigure_vpdn_l2tp_attribute_physical_channel_id(self):
        unconfigure_vpdn_l2tp_attribute_physical_channel_id(self.device)

        self.device.configure.assert_called_once_with(
            ['no vpdn l2tp attribute physical-channel-id']
        )
