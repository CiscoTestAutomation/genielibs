import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prp.configure import (
    unconfigure_prp_sup_vlan_id
)


class TestUnconfigurePrpSupVlanId(unittest.TestCase):

    def test_unconfigure_prp_sup_vlan_id(self):
        device = Mock()

        result = unconfigure_prp_sup_vlan_id(
            device,
            1,
            10
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
           ('no prp channel-group 1 supervisionFrameoption vlan-id 10',)
        )