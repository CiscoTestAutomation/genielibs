import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.rip.configure import (
    configure_rip
)


class TestConfigureRip(unittest.TestCase):

    def test_configure_rip(self):
        device = Mock()

        result = configure_rip(
            device,
            '6.45.45.0'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router rip', 'network 6.45.45.0'],)
        )