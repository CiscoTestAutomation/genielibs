# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# Genie
from genie.libs.ops.rip.iosxr.rip import Rip
from genie.libs.ops.rip.iosxr.tests.rip_output import RipOutput
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail

outputs = {}
outputs.update({'show rip': RipOutput.show_rip})
outputs.update({'show rip vrf VRF1': RipOutput.show_rip_vrf1})
outputs.update({'show rip statistics': RipOutput.show_rip_statistics})
outputs.update({'show rip vrf VRF1 statistics': RipOutput.show_rip_vrf1_statistics})
outputs.update({'show rip database': RipOutput.show_rip_database})
outputs.update({'show rip vrf VRF1 database': RipOutput.show_rip_vrf1_database})
outputs.update({'show rip interface': RipOutput.show_rip_interface})
outputs.update({'show rip vrf VRF1 interface': RipOutput.show_rip_vrf1_interface})


def mapper(key):
    return outputs[key]


class test_rip_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device.connectionmgr.connections['cli'] = self.device

    def test_full_rip(self):
        f = Rip(device=self.device)
        f.maker.outputs[ShowVrfAllDetail] = {'': RipOutput.show_vrf_all_detail}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        f.learn()

        self.maxDiff = None
        self.assertEqual(f.info, RipOutput.rip_ops_output)

    def test_empty_output(self):
        f = Rip(device=self.device)

        # Get outputs
        f.maker.outputs[ShowVrfAllDetail] = {'': {}}

        outputs.update({'show rip': ''})
        outputs.update({'show rip vrf VRF1': ''})
        outputs.update({'show rip statistics': ''})
        outputs.update({'show rip vrf VRF1 statistics': ''})
        outputs.update({'show rip database': ''})
        outputs.update({'show rip vrf VRF1 database': ''})
        outputs.update({'show rip interface': ''})
        outputs.update({'show rip vrf VRF1 interface': ''})

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        f.learn()

        outputs.update({'show rip': RipOutput.show_rip})
        outputs.update({'show rip vrf VRF1':
                        RipOutput.show_rip_vrf1})
        outputs.update({'show rip statistics':
                        RipOutput.show_rip_statistics})
        outputs.update({'show rip vrf VRF1 statistics':
                        RipOutput.show_rip_vrf1_statistics})
        outputs.update({'show rip database':
                        RipOutput.show_rip_database})
        outputs.update({'show rip vrf VRF1 database':
                        RipOutput.show_rip_vrf1_database})
        outputs.update({'show rip interface':
                        RipOutput.show_rip_interface})
        outputs.update({'show rip vrf VRF1 interface':
                        RipOutput.show_rip_vrf1_interface})

        with self.assertRaises(AttributeError):
            f.info['vrf']


if __name__ == '__main__':
    unittest.main()
