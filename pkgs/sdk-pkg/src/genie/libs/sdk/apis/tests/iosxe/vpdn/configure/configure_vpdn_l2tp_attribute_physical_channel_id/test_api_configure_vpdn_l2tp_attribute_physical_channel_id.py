import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vpdn.configure import (
    configure_vpdn_l2tp_attribute_physical_channel_id,
)


class TestConfigureVpdnL2tpAttributePhysicalChannelId(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_vpdn_l2tp_attribute_physical_channel_id(self):
        configure_vpdn_l2tp_attribute_physical_channel_id(self.device)

        self.device.configure.assert_called_once_with(
            ['vpdn l2tp attribute physical-channel-id']
        )
