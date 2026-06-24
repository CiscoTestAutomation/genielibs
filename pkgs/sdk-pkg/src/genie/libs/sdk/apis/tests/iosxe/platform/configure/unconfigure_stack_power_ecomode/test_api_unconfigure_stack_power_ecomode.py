import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_stack_power_ecomode


class TestUnconfigureStackPowerEcomode(unittest.TestCase):

    def test_unconfigure_stack_power_ecomode(self):
        device = Mock()

        result = unconfigure_stack_power_ecomode(
            device,
            'Powerstack-2'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power stack Powerstack-2', 'no ecomode'],)
        )