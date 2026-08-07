import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.rep.configure import (
    unconfigure_rep_ztp
)


class TestUnconfigureRepZtp(unittest.TestCase):

    def test_unconfigure_rep_ztp(self):
        device = Mock()

        result = unconfigure_rep_ztp(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no rep ztp',)
        )