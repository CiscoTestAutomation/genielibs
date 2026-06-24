import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prp.configure import (
    configure_prp_static_vdan_entry_with_vlan
)


class TestConfigurePrpStaticVdanEntryWithVlan(unittest.TestCase):

    def test_configure_prp_static_vdan_entry_with_vlan(self):
        device = Mock()

        result = configure_prp_static_vdan_entry_with_vlan(
            device,
            1,
            '00:00:00:00:00:01',
            10
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('prp channel-group 1 vdanMacaddress 00:00:00:00:00:01 vlan-id 10',)
        )