from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat8k.configure import configure_autoboot


class TestConfigureAutoboot(TestCase):

    def test_configure_autoboot(self):
        device = Mock()
        result = configure_autoboot(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('config-reg 0x2102',)
        )
