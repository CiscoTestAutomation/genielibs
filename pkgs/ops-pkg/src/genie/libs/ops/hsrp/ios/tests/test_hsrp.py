# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.ops.base import Base
from genie.ops.base.maker import Maker
from genie.libs.ops.hsrp.ios.hsrp import Hsrp
from genie.libs.ops.hsrp.ios.tests.hsrp_output import HsrpOutput

# Parser
from genie.libs.parser.ios.show_standby import (
    ShowStandbyInternal,
    ShowStandbyAll,
    ShowStandbyDelay,
)

outputs = {}
outputs['show standby delay'] = HsrpOutput.showStandbyDelayOutput_golden
outputs['show standby all'] = HsrpOutput.showStandbyAllOutput_golden
outputs['show standby internal'] = HsrpOutput.showStandbyInternalOutput_golden

def mapper(key, **kwargs):
    return outputs[key]

class test_hsrp(unittest.TestCase):
    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Create a mock connection to get output for parsing
        self.device_connection = Mock(device=self.device)
        self.device.connectionmgr.connections['cli'] = self.device_connection
        # Set outputs
        self.device_connection.execute.side_effect = mapper

    def test_full(self):
        self.maxDiff = None
        hsrp = Hsrp(device=self.device)
        # Get 'show standby all' output
        hsrp.maker.outputs[ShowStandbyAll] = {"": HsrpOutput.showStandbyAllOutput}
        # Get 'show standby internal' output
        hsrp.maker.outputs[ShowStandbyInternal] = {
            "": HsrpOutput.showStandbyInternalOutput
        }
        # Get 'show standby delay' output
        hsrp.maker.outputs[ShowStandbyDelay] = {"": HsrpOutput.showStandbyDelayOutput}



        # Learn the feature
        hsrp.learn()

        self.assertEqual(hsrp.info, HsrpOutput.hsrpOpsOutput)

    def test_selective_attribute(self):
        self.maxDiff = None
        hsrp = Hsrp(device=self.device)
        # Get 'show standby all' output
        hsrp.maker.outputs[ShowStandbyAll] = {"": HsrpOutput.showStandbyAllOutput}
        # Get 'show standby internal' output
        hsrp.maker.outputs[ShowStandbyInternal] = {
            "": HsrpOutput.showStandbyInternalOutput
        }
        # Get 'show standby delay' output
        hsrp.maker.outputs[ShowStandbyDelay] = {"": HsrpOutput.showStandbyDelayOutput}
        # Get 'show standby delay' output
        hsrp.maker.outputs[ShowStandbyDelay] = {"": HsrpOutput.showStandbyDelayOutput}


        # Learn the feature
        hsrp.learn()

        self.assertEqual(
            99,
            hsrp.info["GigabitEthernet1"]["delay"]["minimum_delay"]
        )

    def test_missing_attributes(self):
        self.maxDiff = None
        hsrp = Hsrp(device=self.device)
        # Get 'show standby all' output
        hsrp.maker.outputs[ShowStandbyAll] = {"": HsrpOutput.showStandbyAllOutput}
        # Get 'show standby internal' output
        hsrp.maker.outputs[ShowStandbyInternal] = {
            "": HsrpOutput.showStandbyInternalOutput
        }
        # Get 'show standby delay' output
        hsrp.maker.outputs[ShowStandbyDelay] = {"": HsrpOutput.showStandbyDelayOutput}



        # Learn the feature
        hsrp.learn()

        with self.assertRaises(KeyError):
            hsrp_bfd_sessions_total = hsrp.info["num_bfd_sessions"]

    def test_incomplete_output(self):
        self.maxDiff = None
        hsrp = Hsrp(device=self.device)
        # Get 'show standby all' output
        hsrp.maker.outputs[ShowStandbyAll] = {"": ""}
        # Get 'show standby internal' output
        hsrp.maker.outputs[ShowStandbyInternal] = {
            "": HsrpOutput.showStandbyInternalOutput
        }
        # Get 'show standby delay' output
        hsrp.maker.outputs[ShowStandbyDelay] = {"": HsrpOutput.showStandbyDelayOutput}



        # Learn the feature
        hsrp.learn()

        with self.assertRaises(KeyError):
            hsrp_groups = hsrp.info["groups"]


if __name__ == "__main__":
    unittest.main()
