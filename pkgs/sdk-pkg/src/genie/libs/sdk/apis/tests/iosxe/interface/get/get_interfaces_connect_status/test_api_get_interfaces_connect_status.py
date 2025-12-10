import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interfaces_connect_status
from unittest.mock import Mock


class TestGetInterfacesConnectStatus(unittest.TestCase):
    
    def test_get_interfaces_connect_status(self):
        self.device = Mock()
        self.device.name = 'TestDevice'        
        self.device.parse = Mock(return_value={
            "interfaces": {
                "TenGigabitEthernet1/1": {"status": "notconnect"},
                "TenGigabitEthernet1/2": {"status": "notconnect"},
                "TenGigabitEthernet1/3": {"status": "notconnect"},
                "GigabitEthernet1/4": {"status": "connected"},
                "GigabitEthernet1/5": {"status": "notconnect"},
                "GigabitEthernet1/6": {"status": "notconnect"},
                "GigabitEthernet1/7": {"status": "notconnect"},
                "GigabitEthernet1/8": {"status": "notconnect"},
                "GigabitEthernet1/9": {"status": "notconnect"},
                "GigabitEthernet1/10": {"status": "notconnect"},
                "GigabitEthernet1/11": {"status": "notconnect"},
                "Ap1/1": {"status": "connected"},
            }
        })
        expected_output = {
            "TenGigabitEthernet1/1": False,
            "TenGigabitEthernet1/2": False,
            "TenGigabitEthernet1/3": False,
            "GigabitEthernet1/4": True,
            "GigabitEthernet1/5": False, 
            "GigabitEthernet1/6": False,
            "GigabitEthernet1/7": False,
            "GigabitEthernet1/8": False,
            "GigabitEthernet1/9": False,
            "GigabitEthernet1/10": False,
            "GigabitEthernet1/11": False,
            "Ap1/1": True,
        }
        output = get_interfaces_connect_status(device=self.device)
        self.assertEqual(output, expected_output)
            
