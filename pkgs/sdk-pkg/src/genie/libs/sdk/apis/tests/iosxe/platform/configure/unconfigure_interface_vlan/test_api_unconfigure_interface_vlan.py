import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_interface_vlan


class TestUnconfigureInterfaceVlan(unittest.TestCase):

    def test_unconfigure_interface_vlan(self):
        device = Mock()

        result = unconfigure_interface_vlan(device, '1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no interface vlan 1',)
        )