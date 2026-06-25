import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_stack_power_auto_off


class TestUnconfigureStackPowerAutoOff(unittest.TestCase):

    def test_unconfigure_stack_power_auto_off(self):
        device = Mock()

        result = unconfigure_stack_power_auto_off(
            device,
            'Powerstack-2'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power stack Powerstack-2', 'no auto-off'],)
        )