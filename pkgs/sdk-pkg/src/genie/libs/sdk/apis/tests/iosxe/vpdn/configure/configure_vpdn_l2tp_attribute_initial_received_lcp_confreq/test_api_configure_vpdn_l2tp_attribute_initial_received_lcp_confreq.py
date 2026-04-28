import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vpdn.configure import (
    configure_vpdn_l2tp_attribute_initial_received_lcp_confreq,
)


class TestConfigureVpdnL2tpAttributeInitialReceivedLcpConfreq(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_vpdn_l2tp_attribute_initial_received_lcp_confreq(self):
        configure_vpdn_l2tp_attribute_initial_received_lcp_confreq(self.device)

        self.device.configure.assert_called_once_with(
            ['vpdn l2tp attribute initial-received-lcp-confreq']
        )
