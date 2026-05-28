import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_interface_VirtualPortGroup


class TestUnconfigureInterfaceVirtualportgroup(unittest.TestCase):

    def test_unconfigure_interface_VirtualPortGroup(self):
        device = Mock()

        result = unconfigure_interface_VirtualPortGroup(device, '1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
             ('no interface VirtualPortGroup 1',)
        )