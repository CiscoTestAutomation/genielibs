import unittest

from pyats.topology import loader

from genie.libs.conf.interface import (
    EthernetInterface,
    TunnelInterface,
    LagInterface,
    VlanInterface)


class TestLoaderInterfaceTypes(unittest.TestCase):

    def test_iosxe_interface_types(self):
        ''' Test the topology loader with different interface types.

        Note: in the current implementation, the type of the interface is
        derived from the name, not the `type` attribute.
        '''
        topology = """
        devices:
            R1:
                os: iosxe
                connections: {}

        topology:
            R1:
                interfaces:
                    Ethernet0/0:
                        type: ethernet
                    Port-channel1:
                        type: port-channel
                    Tunnel10:
                        type: tunnel
                    Vlan100:
                        type: vlan
        """

        expected_interface_data = {
            'Ethernet0/0': {
                'type_name': 'ethernet',
                'type_class': EthernetInterface
            },
            'Port-channel1': {
                'type_name': 'port-channel',
                'type_class': LagInterface
            },
            'Tunnel10': {
                'type_name': 'tunnel',
                'type_class': TunnelInterface
            },
            'Vlan100': {
                'type_name': 'vlan',
                'type_class': VlanInterface
            }
        }

        testbed = loader.load(topology)
        for intf in expected_interface_data:
            intf_type_name = expected_interface_data[intf]['type_name']
            intf_type_class = expected_interface_data[intf]['type_class']
            self.assertEqual(testbed.devices.R1.interfaces[intf].type, intf_type_name)
            self.assertIsInstance(testbed.devices.R1.interfaces[intf],
                                  intf_type_class,
                                  type(testbed.devices.R1.interfaces[intf]))
