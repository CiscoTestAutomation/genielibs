import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    unconfigure_system_mtu
)


class TestUnconfigureSystemMtu(unittest.TestCase):

    def test_unconfigure_system_mtu(self):
        device = Mock()

        result = unconfigure_system_mtu(
            device,
            '9216'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no system mtu 9216',)
        )