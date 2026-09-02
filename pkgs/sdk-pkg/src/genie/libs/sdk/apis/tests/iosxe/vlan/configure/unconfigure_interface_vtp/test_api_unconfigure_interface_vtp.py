import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfigure_interface_vtp


class TestUnconfigureInterfaceVtp(unittest.TestCase):

    def test_unconfigure_interface_vtp(self):
        device = Mock()

        result = unconfigure_interface_vtp(device, 'te1/0/5')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface te1/0/5',
                'no vtp',
            ]
        )
