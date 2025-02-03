from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_macro_description
from unittest.mock import Mock


class TestConfigureInterfaceMacroDescription(TestCase):

    def test_configure_interface_macro_description(self):
        self.device = Mock()
        result = configure_interface_macro_description(self.device, 'TwoGigabitEthernet1/0/21', 'triiger_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TwoGigabitEthernet1/0/21', 'macro description triiger_1'],)
        )
