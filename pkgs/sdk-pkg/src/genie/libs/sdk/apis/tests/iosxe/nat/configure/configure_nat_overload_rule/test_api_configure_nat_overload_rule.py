from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_overload_rule

class TestConfigureNatOverloadRule(TestCase):

    def test_configure_nat_overload_rule(self):
        device = Mock()
        expected_output = (
            'ip nat inside source list test4 interface Loopback100 overload\r\n'
            'ip nat inside source list test4 interface Loopback100 overload\r\n'
        )
        device.configure.return_value = expected_output

        result = configure_nat_overload_rule(device, 'Loopback100', 'test4', True)
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat inside source list test4 interface Loopback100 overload',)
        )

    def test_configure_nat_overload_rule_1(self):
        device = Mock()
        expected_output = (
            'ip nat inside source list test4 interface Loopback100\r\n'
            'ip nat inside source list test4 interface Loopback100\r\n'
        )
        device.configure.return_value = expected_output

        result = configure_nat_overload_rule(device, 'Loopback100', 'test4', False)
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat inside source list test4 interface Loopback100',)
        )