import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_interface_VirtualPortGroup


class TestConfigureInterfaceVirtualportgroup(unittest.TestCase):

    def test_configure_interface_VirtualPortGroup(self):
        device = Mock()

        result = configure_interface_VirtualPortGroup(device, '1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('interface VirtualPortGroup 1',)
        )