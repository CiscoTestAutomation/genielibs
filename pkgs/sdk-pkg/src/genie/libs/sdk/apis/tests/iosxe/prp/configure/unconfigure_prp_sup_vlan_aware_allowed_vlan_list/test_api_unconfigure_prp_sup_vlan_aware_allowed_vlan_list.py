import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prp.configure import (
    unconfigure_prp_sup_vlan_aware_allowed_vlan_list
)


class TestUnconfigurePrpSupVlanAwareAllowedVlanList(unittest.TestCase):

    def test_unconfigure_prp_sup_vlan_aware_allowed_vlan_list(self):
        device = Mock()

        result = unconfigure_prp_sup_vlan_aware_allowed_vlan_list(
            device,
            1
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             ('no prp channel-group 1 supervisionFrameOption vlan-aware-allowed-vlan',)
        )