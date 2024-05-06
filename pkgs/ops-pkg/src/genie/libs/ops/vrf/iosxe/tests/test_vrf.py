# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.vrf.iosxe.vrf import Vrf
from genie.libs.ops.vrf.iosxe.tests.vrf_output import VrfOutput

# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail

outputs = {}
outputs['show vrf detail VRF2'] = VrfOutput.showVrfDetail_vrf2
outputs['show vrf detail'] = VrfOutput.showVrfDetail_all
outputs['show vrf detail Mgmt-vrf'] = VrfOutput.ShowVrfDetail_Mgmt

def mapper(key, **kwargs):
    return outputs[key]


class test_vrf(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        # Create a mock connection to get output for parsing
        self.device_connection = Mock(device=self.device)
        self.device.connectionmgr.connections['cli'] = self.device_connection
        # Set outputs
        self.device_connection.execute.side_effect = mapper

    def test_complete_output(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetail}
        # Learn the feature

        vrf.learn()
        self.maxDiff = None

        # Verify Ops was created successfully
        self.assertDictEqual(vrf.info, VrfOutput.VrfInfo)

    def test_custom_vrf_output(self):
        vrf = Vrf(device=self.device)
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetailCustom}
        # Set outputs

        # Learn the feature
        vrf.learn(vrf='VRF2')
        self.maxDiff = None

        # Verify Ops was created successfully
        self.assertEqual(vrf.info, VrfOutput.VrfCustomInfo)

    def test_custom_vrf_output1(self):
        vrf = Vrf(device=self.device)
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetailCustom1}
        # Set outputs

        # Learn the feature
        vrf.learn(vrf='Mgmt-vrf')
        self.maxDiff = None

        # Verify Ops was created successfully
        self.assertEqual(vrf.info, VrfOutput.VrfCustomInfo1)

    def test_selective_attribute(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetail}

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
