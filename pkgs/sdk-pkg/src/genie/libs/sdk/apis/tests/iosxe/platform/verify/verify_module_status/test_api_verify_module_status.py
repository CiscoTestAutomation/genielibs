import os
import unittest
from textwrap import dedent
from unittest.mock import Mock, call

from genie.conf.base.device import Device
from genie.libs.sdk.apis.iosxe.platform.verify import verify_module_status

class testAPI(unittest.TestCase):

    def test_verify_module_status(self):
        device = Device(name='Router', os='iosxe', custom=dict(abstraction=dict(order=['os'])))
        device.is_connected = Mock(return_value=True)
        device.cli = Mock()
        device.cli.execute = Mock(return_value=dedent('''
        Chassis type: ISR4451-X/K9

        Slot      Type                State                 Insert time (ago) 
        --------- ------------------- --------------------- ----------------- 
        0         ISR4451-X/K9        ok                    00:02:59      
        0/0      ISR4451-X-4x1GE     ok                    00:01:58      
        1         ISR4451-X/K9        ok                    00:02:59      
        2         ISR4451-X/K9        ok                    00:02:59      
        R0        ISR4451-X/K9        ok, active            00:02:59      
        F0        ISR4451-X/K9        ok, active            00:02:59      
        P0        PWR-4450-AC         ok                    00:02:32      
        P1        Unknown             empty                 never         
        P2        ACS-4450-FANASSY    ok                    00:02:32
        P3        ACS-4450-FANASSY    inserted                    00:02:32
        P4        ACS-4450-FANASSY    N/A                    00:02:32

        Slot      CPLD Version        Firmware Version                        
        --------- ------------------- --------------------------------------- 
        0         16092742            16.12(2r)                           
        1         16092742            16.12(2r)                           
        2         16092742            16.12(2r)                           
        R0        16092742            16.12(2r)                           
        F0        16092742            16.12(2r)                           
        '''))
        with self.assertLogs('genie.libs.sdk.apis.iosxe.platform.verify') as cm:
            verify_module_status(device)
            self.assertEqual(cm.output,[
                "INFO:genie.libs.sdk.apis.iosxe.platform.verify:All modules on 'Router' are in stable state"
            ])

        device.cli.execute.assert_has_calls([call('show platform')])

    def test_verify_module_status_negative(self):
        device = Device(name='Router', os='iosxe', custom=dict(abstraction=dict(order=['os'])))
        device.is_connected = Mock(return_value=True)
        device.cli = Mock()
        device.cli.execute = Mock(return_value=dedent('''
        Chassis type: ISR4451-X/K9

        Slot      Type                State                 Insert time (ago) 
        --------- ------------------- --------------------- ----------------- 
        0         ISR4451-X/K9        ok                    00:02:59      
        0/0      ISR4451-X-4x1GE     ok                    00:01:58      
        1         ISR4451-X/K9        ok                    00:02:59      
        2         ISR4451-X/K9        ok                    00:02:59      
        R0        ISR4451-X/K9        fail                  00:02:59      
        F0        ISR4451-X/K9        ok, active            00:02:59      
        P0        PWR-4450-AC         ok                    00:02:32      
        P1        Unknown             empty                 never         
        P2        ACS-4450-FANASSY    ok                    00:02:32      

        Slot      CPLD Version        Firmware Version                        
        --------- ------------------- --------------------------------------- 
        0         16092742            16.12(2r)                           
        1         16092742            16.12(2r)                           
        2         16092742            16.12(2r)                           
        R0        16092742            16.12(2r)                           
        F0        16092742            16.12(2r)                           
        '''))
        with self.assertRaisesRegex(Exception, "Modules on 'Router' are not in stable state"):
            verify_module_status(device, timeout=0.3, interval=0.1)
