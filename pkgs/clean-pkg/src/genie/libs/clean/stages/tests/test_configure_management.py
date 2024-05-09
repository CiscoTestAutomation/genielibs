import unittest

from unittest.mock import call, Mock
from pyats.results import Passed
from pyats.aetest.steps import Steps

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.clean.stages.stages import ConfigureManagement


class TestConfigureManagement(unittest.TestCase):

    def setUp(self):
        self.cls = ConfigureManagement()
        self.device = create_test_device(
            name='aDevice', os='iosxe')

    def test_configure_management(self):
        self.device.management = {
            'interface': 'Gi0/0',
            'vrf': 'Mgmt-vrf',
            'address': {
                'ipv4': '1.1.1.1/24'
            }
        }
        steps = Steps()
        self.cls.configure_management(
            device=self.device,
            steps=steps)
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.configure.assert_has_calls(
            [call(['vrf definition Mgmt-vrf', 'address-family ipv4', 'exit-address-family', 'address-family ipv6', 'exit-address-family']),
             call(['vrf definition Mgmt-vrf', 'address-family ipv4', 'exit-address-family', 'address-family ipv6', 'exit-address-family']),
             call(['interface Gi0/0', 'vrf forwarding Mgmt-vrf', 'ip address 1.1.1.1 255.255.255.0', 'no shutdown'])]
        )

    def test_configure_management_2(self):
        self.device.management = {
            'interface': 'Gi1/0',
            'vrf': 'Mgmt-vrf',
            'dhcp_timeout': 15,
            'address': {
                'ipv4': '2.2.2.2/24'
            },
            'routes': {
                'ipv4': [{
                    'subnet': '192.168.1.0 255.255.255.0',
                    'next_hop': '172.16.1.1'
                    }],
            },
            'protocols': ['http'],
        }
        steps = Steps()
        self.device.execute = Mock()
        self.cls.configure_management(
            device=self.device,
            steps=steps,
            set_hostname=True
            )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.configure.assert_has_calls(
         [call('hostname aDevice'),
          call(['vrf definition Mgmt-vrf', 'address-family ipv4', 'exit-address-family', 'address-family ipv6', 'exit-address-family']),
          call(['vrf definition Mgmt-vrf', 'address-family ipv4', 'exit-address-family', 'address-family ipv6', 'exit-address-family']),
          call(['interface Gi1/0', 'vrf forwarding Mgmt-vrf', 'ip address 2.2.2.2 255.255.255.0', 'no shutdown']),
          call(['ip route vrf Mgmt-vrf 192.168.1.0 255.255.255.0 172.16.1.1']),
          call(['ip http client source-interface Gi1/0'])]
        )
