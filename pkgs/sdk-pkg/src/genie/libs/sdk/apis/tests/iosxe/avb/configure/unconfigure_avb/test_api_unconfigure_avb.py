from unittest import TestCase
from genie.libs.sdk.apis.iosxe.avb.configure import unconfigure_avb
from unittest.mock import Mock, call


class TestUnconfigureAvb(TestCase):

    def test_unconfigure_avb(self):
        self.device = Mock()
        self.device.configure.return_value = None
        result = unconfigure_avb(self.device)
        self.device.configure.assert_called_once_with('no avb')
        expected_output = None
        self.assertEqual(result, expected_output)