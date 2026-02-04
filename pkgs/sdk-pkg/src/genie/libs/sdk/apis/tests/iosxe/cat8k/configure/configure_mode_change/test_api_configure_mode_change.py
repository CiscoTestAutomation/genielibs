from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat8k.configure import configure_mode_change


class TestConfigureModeChange(TestCase):

    def test_configure_mode_change(self):
        device = Mock()
        result = configure_mode_change(device, '0/1', '40G', 60)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('hw-module subslot 0/1 mode 40G',)
        )
