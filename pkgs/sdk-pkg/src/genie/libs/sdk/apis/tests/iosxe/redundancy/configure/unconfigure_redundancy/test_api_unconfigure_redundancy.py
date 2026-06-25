import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.redundancy.configure import (
    unconfigure_redundancy
)


class TestUnconfigureRedundancy(unittest.TestCase):

    def test_unconfigure_redundancy(self):
        device = Mock()

        result = unconfigure_redundancy(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['redundancy', 'mode none'],)
        )