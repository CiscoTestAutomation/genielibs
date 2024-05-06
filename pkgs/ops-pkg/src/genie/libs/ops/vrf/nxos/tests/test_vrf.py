# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.vrf.nxos.vrf import Vrf
from genie.libs.ops.vrf.nxos.tests.vrf_output import VrfOutput

# nxos show_vrf
from genie.libs.parser.nxos.show_vrf import ShowVrfDetail

outputs = {}
outputs['show vrf default detail'] = VrfOutput.showVrfDetail_default
outputs['show vrf all detail'] = VrfOutput.showVrfDetail_all

def mapper(key, **kwargs):
    return outputs[key]


class test_vrf(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
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

        # Verify Ops was created successfully
        self.assertEqual(vrf.info, VrfOutput.VrfInfo)

    def test_custom_output(self):
        vrf = Vrf(device=self.device)
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetailCustom}
        # Set outputs

        # Learn the feature
        vrf.learn(vrf='default')
        self.maxDiff = None

        # Verify Ops was created successfully
        self.assertDictEqual(vrf.info, VrfOutput.VrfCustomInfo)



    def test_selective_attribute(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfDetail] = {'': VrfOutput.ShowVrfDetail}

        # Learn the feature
        vrf.learn()

        # Test specific attributes in info
        self.assertEqual(vrf.info['vrfs']['VRF1']['address_family']['ipv6'], {'table_id': '0x80000003'})

    def test_empty_output(self):
        vrf = Vrf(device=self.device)

        # Set outputs
        vrf.maker.outputs[ShowVrfDetail] = {'': {}}
        outputs['show vrf default detail'] = ''
        outputs['show vrf all detail'] = ''

        # Learn the feature
        vrf.learn()

        # revert back
        outputs['show vrf default detail'] = VrfOutput.showVrfDetail_default
        outputs['show vrf all detail'] = VrfOutput.showVrfDetail_all
        # Check no outputs in vrf.info
        with self.assertRaises(AttributeError):
            neighbor_address = vrf.info['vrfs']['default']['route_distinguisher']


if __name__ == '__main__':
    unittest.main()