import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    unconfigure_stack_mac_persistent_timer
)


class TestUnconfigureStackMacPersistentTimer(unittest.TestCase):

    def test_unconfigure_stack_mac_persistent_timer(self):
        device = Mock()

        result = unconfigure_stack_mac_persistent_timer(
            device
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no stack-mac persistent timer'],)
        )