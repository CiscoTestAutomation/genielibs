#!/usr/bin/env python

import unittest
from unittest.mock import Mock

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


class test_device(TestCase):

    def test_init(self):

        with self.assertNoWarnings():

            Genie.testbed = Testbed()

            with self.assertWarns(UnsupportedDeviceOsWarning,
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

if __name__ == '__main__':
    unittest.main()

