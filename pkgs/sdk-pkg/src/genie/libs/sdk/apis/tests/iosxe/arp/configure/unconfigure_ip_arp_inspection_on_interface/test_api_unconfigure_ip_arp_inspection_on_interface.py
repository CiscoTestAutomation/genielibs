import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_ip_arp_inspection_on_interface


class TestUnconfigureIpArpInspectionOnInterface(unittest.TestCase):

    def test_unconfigure_ip_arp_inspection_on_interface(self):
        device = Mock()
        device.configure = Mock()
        result = unconfigure_ip_arp_inspection_on_interface(
            device=device,
            interface='GigabitEthernet1/0/24',
            type='20'
        )
        self.assertIsNone(result)
        device.configure(['interface GigabitEthernet1/0/24', 'no ip arp inspection limit rate 20'])