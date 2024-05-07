# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.vrf.iosxr.vrf import Vrf
from genie.libs.ops.vrf.iosxr.tests.vrf_output import VrfOutput

from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail

outputs = {}
outputs['show vrf VRF2 detail'] = VrfOutput.showVrfDetail_vrf2
outputs['show vrf all detail'] = VrfOutput.showVrfDetail_all

def mapper(key, **kwargs):
    return outputs[key]


class test_vrf(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Create a mock connection to get output for parsing
        self.device_connection = Mock(device=self.device)
        self.device.connectionmgr.connections['cli'] = self.device_connection
        # Set outputs
        self.device_connection.execute.side_effect = mapper


    def test_complete_output(self):
        vrf = Vrf(device=self.device)
        # Learn the feature
        vrf.maker.outputs[ShowVrfAllDetail] = {'': VrfOutput.ShowVrfAllDetail}

        vrf.learn()

        self.maxDiff = None

        # Verify Ops was created successfully
        self.assertEqual(vrf.info, VrfOutput.VrfInfo)

    def test_custom_output(self):
        vrf = Vrf(device=self.device)
        vrf.maker.outputs[ShowVrfAllDetail] = {'': VrfOutput.ShowVrfAllDetailCustom}
        # Set outputs

        # Learn the feature
        vrf.learn(vrf='VRF2')
        self.maxDiff = None

        # Verify Ops was created successfully
        self.assertDictEqual(vrf.info, VrfOutput.VrfCustomInfo)

    def test_selective_attribute(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfAllDetail] = {'': VrfOutput.ShowVrfAllDetail}

        # Learn the feature
        vrf.learn()

        # Test specific attributes in info
        self.assertEqual('200:1', vrf.info['vrfs']['VRF1']['address_family']['ipv4 unicast']\
                ['route_targets']['200:1']['route_target'])

    def test_empty_output(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfAllDetail] = {'': {}}
        outputs['show vrf VRF2 detail'] = ''
        outputs['show vrf all detail'] = ''

        # Learn the feature
        vrf.learn()

        # revert back
        outputs['show vrf VRF2 detail'] = VrfOutput.showVrfDetail_vrf2
        outputs['show vrf all detail'] = VrfOutput.showVrfDetail_all

        # Check no outputs in vrf.info
        with self.assertRaises(AttributeError):
            route_distingusher = vrf.info['vrfs']['default']['route_distinguisher']


if __name__ == '__main__':
    unittest.main()