from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_boot_manual_switch


class TestConfigureBootManualSwitch(TestCase):

    def test_configure_boot_manual_switch(self):
        device = Mock()
        result = configure_boot_manual_switch(
            device,
            '1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('boot manual switch 1',)
        )