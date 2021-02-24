# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.eigrp.iosxr.eigrp import Eigrp
from genie.libs.ops.eigrp.iosxr.tests.eigrp_output import EigrpOutput

# iosxr show eigrp
from genie.libs.parser.iosxr.show_eigrp import ShowEigrpIpv4NeighborsDetail,\
                                               ShowEigrpIpv6NeighborsDetail

outputs = {}
outputs['show eigrp ipv4 neighbors detail'] = EigrpOutput.ShowEigrpIpv4NeighborsDetail
outputs['show eigrp ipv6 neighbors detail'] = EigrpOutput.ShowEigrpIpv6NeighborsDetail
outputs['show eigrp ipv4 vrf all neighbors detail'] = EigrpOutput.ShowEigrpIpv4NeighborsDetailAllVrf
outputs['show eigrp ipv6 vrf all neighbors detail'] = EigrpOutput.ShowEigrpIpv6NeighborsDetailAllVrf

def mapper(key):
    
    return outputs[key]


class test_eigrp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        # Set outputs
        eigrp.maker.outputs[ShowEigrpIpv4NeighborsDetail] = {
            '': EigrpOutput.ShowEigrpIpv4NeighborsDetail,
            '{"vrf":"all"}': EigrpOutput.ShowEigrpIpv4NeighborsDetailAllVrf,
            }
        eigrp.maker.outputs[ShowEigrpIpv6NeighborsDetail] = {
            '': EigrpOutput.ShowEigrpIpv6NeighborsDetail,
            '{"vrf":"all"}': EigrpOutput.ShowEigrpIpv6NeighborsDetailAllVrf,
            }

        

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        eigrp.learn()

        self.assertEqual(eigrp.info, EigrpOutput.EigrpInfo)

    def test_selective_attribute(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        # Set outputs
        eigrp.maker.outputs[ShowEigrpIpv4NeighborsDetail] = {
            '': EigrpOutput.ShowEigrpIpv4NeighborsDetail,
            '{"vrf":"all"}': EigrpOutput.ShowEigrpIpv4NeighborsDetailAllVrf,
            }
        eigrp.maker.outputs[ShowEigrpIpv6NeighborsDetail] = {
            '': EigrpOutput.ShowEigrpIpv6NeighborsDetail,
            '{"vrf":"all"}': EigrpOutput.ShowEigrpIpv6NeighborsDetailAllVrf,
            }

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        eigrp.learn()

        self.assertEqual(13, eigrp.info['eigrp_instance']['100']['vrf']\
                                      ['VRF1']['address_family']\
                                      ['ipv4']['eigrp_interface']\
                                      ['GigabitEthernet0/0/0/0.390']\
                                      ['eigrp_nbr']['10.12.90.1']['hold'])

    def test_empty_output(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        def empty_mapper(key):
            outputs = {}
            outputs['show eigrp ipv4 neighbors detail'] = ""
            outputs['show eigrp ipv6 neighbors detail'] = ""
            outputs['show eigrp ipv4 vrf all neighbors detail'] = ""
            outputs['show eigrp ipv6 vrf all neighbors detail'] = ""
            return outputs[key]

        # Set outputs
        eigrp.maker.outputs[ShowEigrpIpv4NeighborsDetail] = {
            '': {},
            '{"vrf":"all"}': {},
            }
        eigrp.maker.outputs[ShowEigrpIpv6NeighborsDetail] = {
            '': {},
            '{"vrf":"all"}': {},
            }

        self.device.execute = Mock()
        self.device.execute.side_effect = empty_mapper

        eigrp.learn()

        with self.assertRaises(AttributeError):
            eigrp.info['eigrp_instance']

    def test_missing_attribute(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        # Set outputs
        eigrp.maker.outputs[ShowEigrpIpv4NeighborsDetail] = {'': EigrpOutput.ShowEigrpIpv4NeighborsDetail}
        eigrp.maker.outputs[ShowEigrpIpv6NeighborsDetail] = {'': {}}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        eigrp.learn()

        with self.assertRaises(KeyError):
            eigrp.info['eigrp_instance']['vrf']\
                ['address_family']['eigrp_interface']\
                ['eigrp_nbr']['nbr_sw_ver']


if __name__ == '__main__':
    unittest.main()
