import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prp.configure import (
    configure_prp_sup_vlan_id
)


class TestConfigurePrpSupVlanId(unittest.TestCase):

    def test_configure_prp_sup_vlan_id(self):
        device = Mock()

        result = configure_prp_sup_vlan_id(
            device,
            1,
            10
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             ('prp channel-group 1 supervisionFrameoption vlan-id 10',)
        )