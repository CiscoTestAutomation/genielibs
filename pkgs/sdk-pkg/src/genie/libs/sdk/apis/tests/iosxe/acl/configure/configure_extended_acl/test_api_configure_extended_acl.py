from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_extended_acl


class TestConfigureExtendedAcl(TestCase):

    def test_configure_extended_acl(self):
        self.device = Mock()
        configure_extended_acl(self.device, 'test', 'permit', 'tcp', '2.2.2.2', '4.4.4.4', 3, '0.0.0.255', '0.0.255.255', [])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test', '3 permit tcp 2.2.2.2 0.0.0.255 4.4.4.4 0.0.255.255'],)
        )
    
    def test_configure_extended_acl_1(self):
        self.device = Mock()
        configure_extended_acl(self.device, 'test1', 'deny', 'udp', '2.2.2.2', '4.4.4.4', None, '0.0.0.255', '0.0.255.255', [])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test1', 'deny udp 2.2.2.2 0.0.0.255 4.4.4.4 0.0.255.255'] ,)
        )

    def test_configure_extended_acl_2(self):
        self.device = Mock()
        configure_extended_acl(self.device, 'test2', 'permit', 'icmp', 'any', 'any', None, None, None, [])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test2', 'permit icmp any any'], )
        )

    def test_configure_extended_acl_3(self):
        self.device = Mock()
        configure_extended_acl(self.device, 'test3', 'permit', 'tcp', 'any', 'any', 3, None, None, [])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test3', '3 permit tcp any any'] ,)
        )

    def test_configure_extended_acl_4(self):
        self.device = Mock()
        configure_extended_acl(self.device, 'test4', 'permit', 'icmp', 'any', 'any', None, None, None, [{'match_criteria': 'dscp', 'value': 10}])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test4', 'permit icmp any any dscp 10'] ,)
        )

    def test_configure_extended_acl_5(self):
        self.device = Mock()
        configure_extended_acl(self.device, 'test5', 'deny', 'udp', '2.2.2.2', '4.4.4.4', None, '0.0.0.255', '0.0.255.255', [{'match_criteria': 'range', 'value': '100 500'},
 {'match_criteria': 'dscp', 'value': 40}])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test5', 'deny udp 2.2.2.2 0.0.0.255 4.4.4.4 0.0.255.255 range 100 500 dscp 40'] ,)
        )