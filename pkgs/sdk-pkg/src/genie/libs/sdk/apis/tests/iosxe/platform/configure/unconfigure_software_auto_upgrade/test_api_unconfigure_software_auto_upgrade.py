import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_software_auto_upgrade


class TestUnconfigureSoftwareAutoUpgrade(unittest.TestCase):

    def test_unconfigure_software_auto_upgrade(self):
        device = Mock()

        result = unconfigure_software_auto_upgrade(
            device,
            'enable',
            ''
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no software auto-upgrade enable'],)
        )