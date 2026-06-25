import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_rep_admin_vlan


class TestUnconfigureRepAdminVlan(unittest.TestCase):

    def test_unconfigure_rep_admin_vlan(self):
        device = Mock()

        result = unconfigure_rep_admin_vlan(
            device,
            '2',
            '1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no rep admin vlan 2 segment 1',)
        )