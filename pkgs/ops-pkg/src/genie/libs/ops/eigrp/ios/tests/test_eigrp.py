
# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.eigrp.ios.eigrp import Eigrp
from genie.libs.ops.eigrp.ios.tests.eigrp_output import EigrpOutput

# ios show_eigrp
from genie.libs.parser.iosxe.show_eigrp import (ShowIpEigrpNeighborsDetail,
                                               ShowIpv6EigrpNeighborsDetail)

outputs = {}
outputs['show ip eigrp neighbors detail'] = EigrpOutput.ShowIpEigrpNeighborsDetail_golden
outputs['show ipv6 eigrp neighbors detail'] = EigrpOutput.ShowIpv6EigrpNeighborsDetail_golden

def mapper(key):
    return outputs[key]

class test_eigrp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        # Give the device as as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        # Set outputs
        eigrp.maker.outputs[ShowIpEigrpNeighborsDetail] = {'': EigrpOutput.ShowIpEigrpNeighborsDetail}
        eigrp.maker.outputs[ShowIpv6EigrpNeighborsDetail] = {'': EigrpOutput.ShowIpv6EigrpNeighborsDetail}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        eigrp.learn()

        # Verify Ops was created successfully
        self.assertEqual(eigrp.info, EigrpOutput.EigrpInfo)

    def test_selective_attribute(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        # Set outputs
        eigrp.maker.outputs[ShowIpEigrpNeighborsDetail] = {'': EigrpOutput.ShowIpEigrpNeighborsDetail}
        eigrp.maker.outputs[ShowIpv6EigrpNeighborsDetail] = {'': EigrpOutput.ShowIpv6EigrpNeighborsDetail}

        # Return outputd above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        eigrp.learn()

        self.assertEqual('test', eigrp.info['eigrp_instance']['100']['vrf']\
                                      ['default']['address_family']['ipv4']\
                                      ['name'])

    def test_empty_output(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        # Set outputs
        eigrp.maker.outputs[ShowIpEigrpNeighborsDetail] = {'': {}}
        eigrp.maker.outputs[ShowIpv6EigrpNeighborsDetail] = {'': {}}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        eigrp.learn()

        # Verify attribute is missing
        with self.assertRaises(AttributeError):
            eigrp.info['eigrp_instance']

    def test_missing_attributes(self):
        self.maxDiff = None
        eigrp = Eigrp(device=self.device)

        # Set outputs
        eigrp.maker.outputs[ShowIpEigrpNeighborsDetail] = {'': EigrpOutput.ShowIpEigrpNeighborsDetail}
        eigrp.maker.outputs[ShowIpv6EigrpNeighborsDetail] = {'': {}}

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        eigrp.learn()

        # Veritfy key not created to do output missing

        with self.assertRaises(KeyError):
            single_value_preference = eigrp.info['eigrp_instance']['vrf']\
                ['address_family']['eigrp_interface']\
                ['eigrp_nbr']['nbr_sw_ver']


if __name__ == '__main__':
    unittest.main()
