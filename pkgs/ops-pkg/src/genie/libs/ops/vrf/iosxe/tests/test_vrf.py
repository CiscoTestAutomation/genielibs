# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Genie
from genie.libs.ops.vrf.iosxe.vrf import Vrf
from genie.libs.ops.vrf.iosxe.tests.vrf_output import VrfOutput

# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail


class test_vrf(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device


    def test_complete_output(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetail}

        # Learn the feature
        vrf.learn()
        self.maxDiff = None

        # Verify Ops was created successfully
        self.assertEqual(vrf.info, VrfOutput.VrfInfo)


    def test_selective_attribute(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetail}

        # Learn the feature
        vrf.learn()

        # Test specific attributes in info
        self.assertEqual(vrf.info['vrfs']['VRF1']['address_family']['ipv4 unicast']\
                ['route_targets']['200:1']['route_target'], '200:1')

    def test_empty_output(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfDetail] = {'': {}}

        # Learn the feature
        vrf.learn()

        # Check no outputs in vrf.info
        with self.assertRaises(AttributeError):
            neighbor_address = vrf.info['vrfs']['default']['route_distinguisher']


if __name__ == '__main__':
    unittest.main()