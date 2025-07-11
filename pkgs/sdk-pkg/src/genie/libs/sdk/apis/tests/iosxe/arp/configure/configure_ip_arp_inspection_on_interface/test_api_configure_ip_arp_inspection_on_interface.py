import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import configure_ip_arp_inspection_on_interface


class TestConfigureIpArpInspectionOnInterface(unittest.TestCase):

    def test_configure_ip_arp_inspection_on_interface(self):
        device = Mock()
        device.configure = Mock()
        result = configure_ip_arp_inspection_on_interface(
            device=device,
            interface='GigabitEthernet1/0/24',
            type='limit',
        )
        self.assertIsNone(result)
        device.configure(['interface GigabitEthernet1/0/24', 'ip arp inspection limit rate 20'])