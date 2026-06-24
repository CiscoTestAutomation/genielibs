import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prp.configure import (
    configure_prp_sup_vlan_tagged
)


class TestConfigurePrpSupVlanTagged(unittest.TestCase):

    def test_configure_prp_sup_vlan_tagged(self):
        device = Mock()

        result = configure_prp_sup_vlan_tagged(
            device,
            1
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             ('prp channel-group 1 supervisionFrameOption vlan-tagged',)
        )