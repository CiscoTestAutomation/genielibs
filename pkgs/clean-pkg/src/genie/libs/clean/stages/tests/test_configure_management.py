import unittest

from unittest.mock import call, Mock
from pyats.results import Passed
from pyats.aetest.steps import Steps

from genie.libs.clean.stages.stages import ConfigureInterfaces
from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.clean.stages.stages import ConfigureManagement


class TestConfigureManagement(unittest.TestCase):

    def setUp(self):
        self.cls = ConfigureManagement()
        self.device = create_test_device(name='aDevice',
                                         os='iosxe',
                                         alias="deviceAlias")

    def test_configure_management(self):
        self.device.management = {
            'interface': 'Gi0/0',
            'vrf': 'Mgmt-vrf',
            'address': {
                'ipv4': '1.1.1.1/24'
            }
        }
        steps = Steps()
        self.cls.configure_management(device=self.device, steps=steps)
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.configure.assert_has_calls([
            call([
                'vrf definition Mgmt-vrf', 'address-family ipv4',
                'exit-address-family', 'address-family ipv6',
                'exit-address-family'
            ]),
            call([
                'vrf definition Mgmt-vrf', 'address-family ipv4',
                'exit-address-family', 'address-family ipv6',
                'exit-address-family'
            ]),
            call([
                'interface Gi0/0', 'vrf forwarding Mgmt-vrf',
                'ip address 1.1.1.1 255.255.255.0', 'no shutdown'
            ])
        ])

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
        self.cls.configure_management(device=self.device,
                                      steps=steps,
                                      set_hostname=True)
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.configure.assert_has_calls([
            call('hostname aDevice'),
            call([
                'vrf definition Mgmt-vrf', 'address-family ipv4',
                'exit-address-family', 'address-family ipv6',
                'exit-address-family'
            ]),
            call([
                'vrf definition Mgmt-vrf', 'address-family ipv4',
                'exit-address-family', 'address-family ipv6',
                'exit-address-family'
            ]),
            call([
                'interface Gi1/0', 'vrf forwarding Mgmt-vrf',
                'ip address 2.2.2.2 255.255.255.0', 'no shutdown'
            ]),
            call([
                'ip route vrf Mgmt-vrf 192.168.1.0 255.255.255.0 172.16.1.1'
            ]),
            call(['ip http client source-interface Gi1/0'])
        ])

    def test_configure_management_alias_hostname(self):
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
            set_hostname=True,
            alias_as_hostname=True,
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.configure.assert_has_calls([call('hostname deviceAlias')])

    def test_configure_management_ping_gateway(self):
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
            'gateway': {
                'ipv4': '2.2.2.2'
            },
            'protocols': ['http'],
        }
        steps = Steps()
        self.device.ping = Mock()
        self.cls.ping_gateway(
            device=self.device,
            steps=steps,
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.ping.assert_has_calls([
            call(addr='2.2.2.2',
                 vrf='Mgmt-vrf',
                 source='Gi1/0',
                 timeout=30,
                 count=5)
        ], )

    def test_configure_management_check_management_interface_status(self):
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
            'gateway': {
                'ipv4': '2.2.2.2'
            },
            'protocols': ['http'],
        }
        steps = Steps()
        self.device.parse = Mock()
        self.device.parse = Mock(return_value={
            'Gi1/0': {
                'oper_status': 'up',
                'protocol_status': 'up'
            }
        })
        self.cls.check_management_interface_status(
            device=self.device,
            steps=steps,
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.parse.assert_has_calls([call('show interface Gi1/0')])

    def test_configure_management_ping_gateway_ipv6(self):
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
            'gateway': {
                'ipv4': '2.2.2.2',
                'ipv6': '1.1.1.1'
            },
            'protocols': ['http'],
        }
        steps = Steps()
        self.device.ping = Mock()
        self.cls.ping_gateway(
            device=self.device,
            steps=steps,
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.ping.assert_has_calls([
            call(addr='2.2.2.2',
                 vrf='Mgmt-vrf',
                 source='Gi1/0',
                 timeout=30,
                 count=5),
            call(addr='1.1.1.1',
                 vrf='Mgmt-vrf',
                 source='Gi1/0',
                 timeout=30,
                 count=5),
        ], )

class TestConfigureInterfaces(unittest.TestCase):

    def setUp(self):
        self.cls = ConfigureInterfaces()
        self.device = Mock()
        self.device.interfaces = {}
        self.device.custom_config_cli = None
        self.device.build_config = None

    def test_configure_interfaces_name_match(self):
        # Mock interface object
        iface_obj = Mock()
        iface_obj.name = 'GigabitEthernet0/1'
        iface_obj.alias = 'mgmt0'
        iface_obj.enabled = None
        iface_obj.breakout = False
        iface_obj.build_config = Mock(return_value='interface Gi0/1\n no shutdown')

        self.device.interfaces = {'GigabitEthernet0/1': iface_obj}

        # Interface matches by name
        interfaces = {'GigabitEthernet0/1': {'attributes': ['enabled']}}
        steps = Steps()
        self.cls.configure_interfaces(device=self.device, steps=steps, interfaces=interfaces)

        iface_obj.build_config.assert_called_once_with(attributes={'enabled': True}, apply=False)
        self.device.configure.assert_called_once_with(['interface Gi0/1', ' no shutdown'])

    def test_configure_interfaces_alias_match(self):
        # Mock interface object
        iface_obj = Mock()
        iface_obj.name = 'GigabitEthernet0/2'
        iface_obj.alias = 'mgmt0'
        iface_obj.enabled = None
        iface_obj.breakout = False
        iface_obj.build_config = Mock(return_value='interface Gi0/2\n no shutdown')

        self.device.interfaces = {'GigabitEthernet0/2': iface_obj}

        # Interface matches by alias
        interfaces = {'mgmt0': {'attributes': ['enabled']}}
        steps = Steps()
        self.cls.configure_interfaces(device=self.device, steps=steps, interfaces=interfaces)

        iface_obj.build_config.assert_called_once_with(attributes={'enabled': True}, apply=False)
        self.device.configure.assert_called_once_with(['interface Gi0/2', ' no shutdown'])

