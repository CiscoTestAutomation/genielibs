import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prp.configure import (
    configure_prp_sup_vlan_aware_reject_untagged
)


class TestConfigurePrpSupVlanAwareRejectUntagged(unittest.TestCase):

    def test_configure_prp_sup_vlan_aware_reject_untagged(self):
        device = Mock()

        result = configure_prp_sup_vlan_aware_reject_untagged(
            device,
            1
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('prp channel-group 1 supervisionFrameOption vlan-aware-reject-untagged',)
        )