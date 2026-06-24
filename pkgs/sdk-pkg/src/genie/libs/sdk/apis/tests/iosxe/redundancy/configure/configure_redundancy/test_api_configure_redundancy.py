import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.redundancy.configure import (
    configure_redundancy
)


class TestConfigureRedundancy(unittest.TestCase):

    def test_configure_redundancy(self):
        device = Mock()

        result = configure_redundancy(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['redundancy', 'mode sso'],)
        )