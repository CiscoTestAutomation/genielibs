from unittest import TestCase
from genie.libs.sdk.apis.iosxe.avb.configure import configure_avb
from unittest.mock import Mock, call


class TestConfigureAvb(TestCase):

    def test_configure_avb(self):
        self.device = Mock()
        self.device.configure.return_value = None

        result = configure_avb(self.device)

        self.device.configure.assert_called_once_with('avb')
        expected_output = None
        self.assertEqual(result, expected_output)