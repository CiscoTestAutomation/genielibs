import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    configure_stack_mac_persistent_timer
)


class TestConfigureStackMacPersistentTimer(unittest.TestCase):

    def test_configure_stack_mac_persistent_timer(self):
        device = Mock()

        result = configure_stack_mac_persistent_timer(
            device,
            '3'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('stack-mac persistent timer 3',)
        )