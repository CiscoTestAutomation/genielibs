# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.eigrp.nxos.eigrp import Eigrp
from genie.libs.ops.eigrp.nxos.tests.eigrp_output import EigrpOutput

# nxos show eigrp
from genie.libs.parser.nxos.show_eigrp import ShowIpv4EigrpNeighborsDetail,\
                                              ShowIpv6EigrpNeighborsDetail

outputs = {}
outputs['show ip eigrp neighbors detail vrf all'] = EigrpOutput.ShowIpv4EigrpNeighborsDetail
outputs['show ipv6 eigrp neighbors detail vrf all'] = EigrpOutput.ShowIpv6EigrpNeighborsDetail


def mapper(key):
    return outputs[key]


class test_eigrp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        # Set outputs
        eigrp.maker.outputs[ShowIpv4EigrpNeighborsDetail] = {'': EigrpOutput.ShowIpv4EigrpNeighborsDetail}
        eigrp.maker.outputs[ShowIpv6EigrpNeighborsDetail] = {'': EigrpOutput.ShowIpv6EigrpNeighborsDetail}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        eigrp.learn()

        self.assertEqual(eigrp.info, EigrpOutput.EigrpInfo)

    def test_selective_attribute(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        eigrp.maker.outputs[ShowIpv4EigrpNeighborsDetail] = {'': EigrpOutput.ShowIpv4EigrpNeighborsDetail}
        eigrp.maker.outputs[ShowIpv6EigrpNeighborsDetail] = {'': EigrpOutput.ShowIpv6EigrpNeighborsDetail}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        eigrp.learn()

        self.assertEqual(1, eigrp.info['eigrp_instance']['100']['vrf']
                         ['default']['address_family']['ipv4']
                         ['eigrp_interface']['Ethernet1/2.90']
                         ['eigrp_nbr']['10.13.90.1']['peer_handle'])

    def test_empty_output(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        eigrp.maker.outputs[ShowIpv4EigrpNeighborsDetail] = {'': {}}
        eigrp.maker.outputs[ShowIpv6EigrpNeighborsDetail] = {'': {}}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        eigrp.learn()

        with self.assertRaises(AttributeError):
            eigrp.info['eigrp_instance']

    def test_missing_attributes(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        eigrp.maker.outputs[ShowIpv4EigrpNeighborsDetail] = {'': EigrpOutput.ShowIpv4EigrpNeighborsDetail}
        eigrp.maker.outputs[ShowIpv6EigrpNeighborsDetail] = {'': {}}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        eigrp.learn()

        with self.assertRaises(KeyError):
            eigrp.info['eigrp_instance']['vrf']\
                ['address_family']['eigrp_interface']\
                ['eigrp_nbr']['nbr_sw_ver']


if __name__ == '__main__':
    unittest.main()
