import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prp.configure import (
    configure_prp_sup_vlan_aware_allowed_vlan_list
)


class TestConfigurePrpSupVlanAwareAllowedVlanList(unittest.TestCase):

    def test_configure_prp_sup_vlan_aware_allowed_vlan_list(self):
        device = Mock()

        result = configure_prp_sup_vlan_aware_allowed_vlan_list(
            device,
            1,
            10
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             ('prp channel-group 1 supervisionFrameOption vlan-aware-allowed-vlan 10',)
        )