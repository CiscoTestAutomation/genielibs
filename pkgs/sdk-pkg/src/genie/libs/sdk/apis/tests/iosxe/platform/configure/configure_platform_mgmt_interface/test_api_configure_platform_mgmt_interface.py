import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_platform_mgmt_interface


class TestConfigurePlatformMgmtInterface(unittest.TestCase):

    def test_configure_platform_mgmt_interface(self):
        device = Mock()

        result = configure_platform_mgmt_interface(device, 'te0/1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('platform management-interface te0/1',)
        )