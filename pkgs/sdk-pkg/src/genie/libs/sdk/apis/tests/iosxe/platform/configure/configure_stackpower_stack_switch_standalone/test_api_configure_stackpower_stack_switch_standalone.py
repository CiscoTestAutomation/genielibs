import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_stackpower_stack_switch_standalone


class TestConfigureStackpowerStackSwitchStandalone(unittest.TestCase):

    def test_configure_stackpower_stack_switch_standalone(self):
        device = Mock()

        result = configure_stackpower_stack_switch_standalone(device, 1, 'Powerstack-Ring-1', False)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power switch 1', 'stack Powerstack-Ring-1', 'no standalone'],)
        )