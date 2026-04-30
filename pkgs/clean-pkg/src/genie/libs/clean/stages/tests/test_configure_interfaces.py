import unittest

from unittest.mock import call, Mock
from pyats.results import Passed
from pyats.aetest.steps import Steps
from ipaddress import IPv4Address
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
        self.svl_devices = create_test_device(
            name='aDevice', os='iosxe', platform='cat9k',
            model='c9500', chassis_type='stackwise_virtual')

    def test_configure_interfaces(self):
        intf = PhysicalInterface(device=self.device, name='GigabitEthernet0/0')
        self.device.interfaces = {
            'GigabitEthernet0/0': intf
        }
        steps = Steps()

        self.cls.configure_interfaces(
            device=self.device,
            steps=steps)

        self.assertTrue(intf.enabled)

    def test_configure_invalid_device(self):
        intf = BasePhysicalInterface(device=self.invalid_device, name='GigabitEthernet0/0')
        self.invalid_device.interfaces = {
            'GigabitEthernet0/0': intf
        }
        steps = Steps()
        self.cls.configure_interfaces(
            device=self.invalid_device,
            steps=steps)

        self.assertTrue(intf.enabled)

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
        
    def test_skip_svl_configure_interfaces(self):
        intf = DetailedPhysicalInterface(device=self.device, name='GigabitEthernet0/0')
        intf.stackwise_virtual_link = 'True'
        self.svl_devices.configure = Mock()
        
        self.svl_devices.interfaces = {
            'GigabitEthernet0/0': intf}

        steps = Steps()

        self.cls.configure_interfaces(
            device=self.svl_devices,
            steps=steps)
        self.svl_devices.configure.assert_not_called()

    def test_ipv4_disables_switchport(self):

        intf = PhysicalInterface(device=self.device, name='GigabitEthernet1/0/1')
        intf.ipv4 = IPv4Address('10.1.1.1')
        self.device.interfaces = {
            'GigabitEthernet1/0/1': intf
        }
        steps = Steps()

        self.cls.configure_interfaces(
            device=self.device,
            steps=steps,
            interfaces={
                '.*': {
                    'attributes': ['enabled', 'ipv4', 'switchport', 'breakout']
                }
            })

        self.assertFalse(intf.switchport)
        self.device.configure.assert_called_once()
        config_lines = self.device.configure.call_args[0][0]
        self.assertIn('no switchport', '\n'.join(config_lines))