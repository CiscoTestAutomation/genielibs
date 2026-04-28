from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_hw_module_switch_number_ecomode_led


class TestConfigureHwModuleSwitchNumberEcomodeLed(TestCase):

    def test_configure_hw_module_switch_number_ecomode_led(self):
        device = Mock()
        result = configure_hw_module_switch_number_ecomode_led(
            device,
            '1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['hw-module switch 1 ecomode led'],)
        )