import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_boot_system


class TestUnconfigureBootSystem(unittest.TestCase):

    def test_unconfigure_boot_system(self):
        device = Mock()

        result = unconfigure_boot_system(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no boot system',)
        )