#!/usr/bin/env python

import unittest
from unittest.mock import Mock, MagicMock, call

from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device

from genie.libs.conf.device import UnsupportedDeviceOsWarning
from genie.libs.conf.device import Device as XbuDevice
from genie.libs.conf.device.ios import Device as IosDevice
from genie.libs.conf.device.iosxe import Device as IosxeDevice
from genie.libs.conf.device.iosxr import Device as IosxrDevice
from genie.libs.conf.device.nxos import Device as NxosDevice
from genie.libs.conf.device.tgen import Device as TgenDevice
from genie.libs.conf.device.hltapi import Device as HltapiDevice
from genie.libs.conf.device.agilent import Device as AgilentDevice
from genie.libs.conf.device.ixia import Device as IxiaDevice
from genie.libs.conf.device.pagent import Device as PagentDevice
from genie.libs.conf.device.spirent import Device as SpirentDevice

from genie.libs.conf.tests.device.interface_output import InterfaceOutput
class test_device(TestCase):

    def test_init(self):

        with self.assertNoWarnings():

            Genie.testbed = Testbed()
            # added DeprecationWarning for the issue with import __namespace__
            with self.assertWarns((UnsupportedDeviceOsWarning, DeprecationWarning),
                                  msg='Device PE1 OS is unknown; Extended Device functionality will not be available: mandatory field \'os\' was  not given in the yaml file'):
                dev1 = Device(name='PE1')
            self.assertIsInstance(dev1, Device)
            self.assertIsInstance(dev1, XbuDevice)
            self.assertIs(type(dev1), XbuDevice)

            self.assertIsInstance(dev1, Device)
            self.assertIsInstance(dev1, XbuDevice)
            self.assertIs(type(dev1), XbuDevice)

            dev1 = Device(name='PE1', os='ios')
            self.assertIsInstance(dev1, Device)
            self.assertIsInstance(dev1, XbuDevice)
            self.assertIsInstance(dev1, IosDevice)

            dev1 = Device(name='PE1', os='iosxe')
            self.assertIsInstance(dev1, Device)
            self.assertIsInstance(dev1, XbuDevice)
            self.assertIsInstance(dev1, IosxeDevice)

            dev1 = Device(name='PE1', os='iosxr')
            self.assertIsInstance(dev1, Device)
            self.assertIsInstance(dev1, XbuDevice)
            self.assertIsInstance(dev1, IosxrDevice)

            dev1 = Device(name='PE1', os='nxos')
            self.assertIsInstance(dev1, Device)
            self.assertIsInstance(dev1, XbuDevice)
            self.assertIsInstance(dev1, NxosDevice)

            dev1 = Device(name='PE1', os='agilent')
            self.assertIsInstance(dev1, Device)
            self.assertIsInstance(dev1, XbuDevice)
            self.assertIsInstance(dev1, TgenDevice)
            self.assertIsInstance(dev1, HltapiDevice)
            self.assertIsInstance(dev1, AgilentDevice)

            dev1 = Device(name='PE1', os='ixia')
            self.assertIsInstance(dev1, Device)
            self.assertIsInstance(dev1, XbuDevice)
            self.assertIsInstance(dev1, TgenDevice)
            self.assertIsInstance(dev1, HltapiDevice)
            self.assertIsInstance(dev1, IxiaDevice)

            dev1 = Device(name='PE1', os='pagent')
            self.assertIsInstance(dev1, Device)
            self.assertIsInstance(dev1, XbuDevice)
            self.assertIsInstance(dev1, TgenDevice)
            self.assertIsInstance(dev1, HltapiDevice)
            self.assertIsInstance(dev1, PagentDevice)

            dev1 = Device(name='PE1', os='spirent')
            self.assertIsInstance(dev1, Device)
            self.assertIsInstance(dev1, XbuDevice)
            self.assertIsInstance(dev1, TgenDevice)
            self.assertIsInstance(dev1, HltapiDevice)
            self.assertIsInstance(dev1, SpirentDevice)

    def test_htlapi_traffic_control(self):
        dev = Device(name='ixia', os='hltapi')
        dev.default = MagicMock()
        dev.traffic_control(param='value')
        dev.default.traffic_control.assert_has_calls([call(param='value')])
        
class TestLearnInterface(unittest.TestCase):
        
    def test_learn_interfaces_iosxe(self):
        self.dev1 = Device(name='PE1', os='iosxe')
        xe_interfaces = {'GigabitEthernet0/1/0', 'GigabitEthernet0/0/1', 'GigabitEthernet0/0/0', 'GigabitEthernet1/0/1', 'GigabitEthernet1/0/2', 'GigabitEthernet0/2/0'}
        
        self.dev1.learn = MagicMock()
        learn_1_return_value = MagicMock()
        learn_1_return_value.to_dict = MagicMock(return_value=InterfaceOutput.IosxeInterfaceOutput_info)
        self.dev1.learn.return_value = learn_1_return_value
        self.dev1.api.is_management_interface = MagicMock(return_value=False)
        self.assertEqual(len(self.dev1.interfaces), 0)
        self.dev1.learn_interfaces()
        self.assertEqual(set(self.dev1.interfaces.keys()), xe_interfaces)

    def test_learn_interfaces_iosxr(self): 
        self.dev2 = Device(name='PE1', os='iosxr')
        xr_interfaces = {'Null0', 'GigabitEthernet0/0/0/5', 'GigabitEthernet0/0/0/0.20', 'GigabitEthernet0/0/0/4', 'GigabitEthernet0/0/0/0.10', 'MgmtEth0/0/CPU0/0', 
                        'GigabitEthernet0/0/0/6', 'GigabitEthernet0/0/0/1', 'GigabitEthernet0/0/0/0', 'GigabitEthernet0/0/0/2', 'GigabitEthernet0/0/0/3'}    
        self.dev2.learn = MagicMock()
        learn_2_return_value = MagicMock()
        learn_2_return_value.to_dict = MagicMock(return_value=InterfaceOutput.IosxrInterfaceOpsOutput_info)
        self.dev2.learn.return_value = learn_2_return_value
        self.dev2.api.is_management_interface = MagicMock(return_value=False)
        self.assertEqual(len(self.dev2.interfaces), 0)
        self.dev2.learn_interfaces()
        self.assertEqual(set(self.dev2.interfaces.keys()), xr_interfaces)
        # self.dev3.learn.side_effect = InterfaceOutput.NxosInterfaceOpsOutput_info

    def test_learn_interfaces_nxos(self): 
        self.dev3 = Device(name='PE1', os='nxos')
        xr_interfaces = {'Ethernet1/17', 'Mgmt0', 'Ethernet1/15', 'Ethernet1/18', 'Null0', 'Ethernet1/10', 'Ethernet1/12', 'Ethernet1/1', 
                         'Ethernet2/1', 'Ethernet1/13', 'Ethernet1/14', 'Ethernet1/16', 'Ethernet1/11'}    
        self.dev3.learn = MagicMock()
        learn_3_return_value = MagicMock()
        learn_3_return_value.to_dict = MagicMock(return_value=InterfaceOutput.NxosInterfaceOpsOutput_info)
        self.dev3.learn.return_value = learn_3_return_value
        self.dev3.api.is_management_interface = MagicMock(return_value=False)
        self.assertEqual(len(self.dev3.interfaces), 0)
        self.dev3.learn_interfaces()
        self.assertEqual(set(self.dev3.interfaces.keys()), xr_interfaces)

if __name__ == '__main__':
    unittest.main()

