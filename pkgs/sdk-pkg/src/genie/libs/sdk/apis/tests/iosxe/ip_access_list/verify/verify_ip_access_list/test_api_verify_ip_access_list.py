from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ip_access_list.verify import (
    verify_ip_access_list
)


class TestVerifyIpAccessList(TestCase):

    def test_verify_ip_access_list(self):
        self.device = Mock()
        acl_name = 'xACSACLx-IP-mixed_acl_isr1k-63abbefa'
        results_map = {
            f'show ip access-lists {acl_name}':'''
10 permit udp any eq 6000 any eq 6000
2 deny udp any host 100.0.0.10
3 deny icmp any any
4 permit tcp any host 100.0.0.11 eq 7001'''
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = verify_ip_access_list(
            self.device, acl_name, '3 deny icmp any any'
        )
        self.assertIn(
            f'show ip access-lists {acl_name}',
            self.device.execute.call_args_list[0][0]
        )
        self.assertTrue(result)
        result = verify_ip_access_list(
            self.device, acl_name, '3 deny tcp any any'
        )
        self.assertFalse(result)
        result = verify_ip_access_list(
            self.device, acl_name,
            '0 permit udp any eq 6000 any eq 6000'
        )
        self.assertFalse(result)
        result = verify_ip_access_list(
            self.device, acl_name, ['3 deny icmp any any']
        )
        self.assertTrue(result)
        result = verify_ip_access_list(
            self.device, acl_name,
            [
                '3 deny icmp any any',
                '4 permit tcp any host 100.0.0.11 eq 7001'
            ]
        )
        self.assertTrue(result)
        result = verify_ip_access_list(
            self.device, acl_name,
            [
                '3 deny icmp any any',
                '4 permit tcp any host 100.0.0.12 eq 7001'
            ]
        )
        self.assertFalse(result)
