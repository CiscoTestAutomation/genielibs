from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.configure import (
    unconfigure_aaa_accounting_network_default_group,
)


class TestUnconfigureAaaAccountingNetworkDefaultGroup(TestCase):

    def test_unconfigure_aaa_accounting_network_default_group(self):
        self.device = Mock()
        unconfigure_aaa_accounting_network_default_group(self.device, 'radius')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no aaa accounting network default group radius',)
        )
