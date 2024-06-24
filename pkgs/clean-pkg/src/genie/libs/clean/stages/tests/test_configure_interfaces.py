import unittest

from unittest.mock import call, Mock
from pyats.results import Passed
from pyats.aetest.steps import Steps

from genie.libs.conf.interface import PhysicalInterface as BasePhysicalInterface
from genie.libs.conf.interface.iosxe.interface import PhysicalInterface
from genie.libs.conf.interface.iosxe.cat9k.c9500.c9500_28C8D.interface import PhysicalInterface as DetailedPhysicalInterface
from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.clean.stages.stages import ConfigureInterfaces


class TestConfigureInterfaces(unittest.TestCase):

    def setUp(self):
        self.cls = ConfigureInterfaces()
        self.device = create_test_device(
            name='aDevice', os='iosxe')
        self.invalid_device = create_test_device(
            name='aDevice', os='invalid')
        self.detailed_devices = create_test_device(
            name='aDevice', os='iosxe', platform='cat9k', 
            model='c9500', pid='C9500X-28C8D')
        
    def test_configure_interfaces(self):
        intf = PhysicalInterface(device=self.device, name='GigabitEthernet0/0')
        self.device.interfaces = {
            'GigabitEthernet0/0': intf
        }
        steps = Steps()

        self.cls.configure_interfaces(
            device=self.device,
            steps=steps)
        
        self.assertIsNone(intf.enabled)

    def test_configure_invalid_device(self):
        intf = BasePhysicalInterface(device=self.invalid_device, name='GigabitEthernet0/0')
        self.invalid_device.interfaces = {
            'GigabitEthernet0/0': intf
        }
        steps = Steps()
        self.cls.configure_interfaces(
            device=self.invalid_device,
            steps=steps)

        self.assertIsNone(intf.enabled)

    def test_configure_detailed_interfaces(self):
        intf = DetailedPhysicalInterface(device=self.device, name='GigabitEthernet0/0')
        intf.breakout = 'True'
        self.detailed_devices.interfaces = {
            'GigabitEthernet0/0': intf
        }
        steps = Steps()

        self.cls.configure_interfaces(
            device=self.detailed_devices,
            steps=steps)
        
        self.assertEqual(self.device.custom_config_cli, '\nhw-module breakout 0')