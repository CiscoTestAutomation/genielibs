from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import unconfigure_bfd_interval
from unittest.mock import Mock


class TestUnconfigureBfdInterval(TestCase):

    def test_unconfigure_bfd_interval(self):
        self.device = Mock()
        self.device.configure.return_value = None

        interface = 'GigabitEthernet1/0/1'

        result = unconfigure_bfd_interval(self.device, interface)

        self.device.configure.assert_called_once_with([
            'interface GigabitEthernet1/0/1',
            'no bfd interval'
        ])

        expected_output = None
        self.assertEqual(result, expected_output)
