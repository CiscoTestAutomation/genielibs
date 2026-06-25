import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.prp.configure import (
    unconfigure_prp_static_vdan_entry
)


class TestUnconfigurePrpStaticVdanEntry(unittest.TestCase):

    def test_unconfigure_prp_static_vdan_entry(self):
        device = Mock()

        result = unconfigure_prp_static_vdan_entry(
            device,
            1,
            '00:00:00:00:00:01'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no prp channel-group 1 vdanMacaddress 00:00:00:00:00:01',)
        )