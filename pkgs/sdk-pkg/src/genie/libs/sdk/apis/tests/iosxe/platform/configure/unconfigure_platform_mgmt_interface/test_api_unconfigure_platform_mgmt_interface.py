import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_platform_mgmt_interface


class TestUnconfigurePlatformMgmtInterface(unittest.TestCase):

    def test_unconfigure_platform_mgmt_interface(self):
        device = Mock()

        result = unconfigure_platform_mgmt_interface(device, 'te0/1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no platform management-interface te0/1',)
        )