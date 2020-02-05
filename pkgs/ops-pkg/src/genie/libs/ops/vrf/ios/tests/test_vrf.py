# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.vrf.ios.vrf import Vrf
from genie.libs.ops.vrf.ios.tests.vrf_output import VrfOutput

# iosxe show_vrf
from genie.libs.parser.ios.show_vrf import ShowVrfDetail

outputs = {}
outputs['show vrf detail VRF2'] = VrfOutput.showVrfDetail_vrf2
outputs['show vrf detail'] = VrfOutput.showVrfDetail_all

def mapper(key):
    return outputs[key]


class test_vrf(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device
    def test_complete_output(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetail}
        # Learn the feature
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        vrf.learn()
        self.maxDiff = None

        # Verify Ops was created successfully
        self.assertDictEqual(vrf.info, VrfOutput.VrfInfo)

    def test_custom_vrf_output(self):
        vrf = Vrf(device=self.device)
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetailCustom}
        # Set outputs
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        vrf.learn(vrf='VRF2')
        self.maxDiff = None

        # Verify Ops was created successfully
        self.assertEqual(vrf.info, VrfOutput.VrfCustomInfo)

    def test_selective_attribute(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetail}
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        vrf.learn()

        # Test specific attributes in info
        self.assertEqual(vrf.info['vrfs']['VRF1']['address_family']['ipv4 unicast'] \
                             ['route_targets']['200:1']['route_target'], '200:1')

    def test_empty_output(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfDetail] = {'': {}}
        outputs['show vrf detail VRF2'] = ''
        outputs['show vrf detail'] = ''
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        vrf.learn()

        # revert back
        outputs['show vrf detail VRF2'] = VrfOutput.showVrfDetail_vrf2
        outputs['show vrf detail'] = VrfOutput.showVrfDetail_all
        # Check no outputs in vrf.info
        with self.assertRaises(AttributeError):
            neighbor_address = vrf.info['vrfs']['default']['route_distinguisher']


if __name__ == '__main__':
    unittest.main()
