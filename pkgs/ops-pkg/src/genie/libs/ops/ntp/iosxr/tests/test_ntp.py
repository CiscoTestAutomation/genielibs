# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.ntp.iosxr.ntp import Ntp
from genie.libs.ops.ntp.iosxr.tests.ntp_output import NtpOutput

# Parser
from genie.libs.parser.iosxr.show_ntp import ShowNtpAssociations, \
                                             ShowNtpStatus, \
                                             ShowRunningConfigNtp


class test_ntp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        ntp = Ntp(device=self.device)
        # Get outputs
        ntp.maker.outputs[ShowNtpAssociations] = \
            {"": NtpOutput.ShowNtpAssociations}

        ntp.maker.outputs[ShowNtpStatus] = \
            {"": NtpOutput.ShowNtpStatus}

        ntp.maker.outputs[ShowRunningConfigNtp] = \
            {"": NtpOutput.ShowRunningConfigNtp}

        # Learn the feature
        ntp.learn()

        # Verify Ops was created successfully
        self.assertEqual(ntp.info, NtpOutput.Ntp_info)

        # Check specific attribute values
        # info - clock_state
        self.assertEqual(ntp.info['clock_state']['system_status']\
            ['clock_state'], 'synchronized')
        # info - vrf default
        self.assertEqual(ntp.info['vrf']['default']['unicast_configuration']\
            ['address']['127.127.1.1']['type']['server']['type'], 'server')

    def test_empty_output(self):
        self.maxDiff = None
        ntp = Ntp(device=self.device)
        # Get outputs
        ntp.maker.outputs[ShowNtpAssociations] = \
            {"": {}}

        ntp.maker.outputs[ShowNtpStatus] = \
            {"": {}}

        ntp.maker.outputs[ShowRunningConfigNtp] = \
            {"": {}}

        # Learn the feature
        ntp.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            ntp.info['vrf']

    def test_incomplete_output(self):
        self.maxDiff = None

        ntp = Ntp(device=self.device)

        # Get outputs
        ntp.maker.outputs[ShowNtpAssociations] = \
            {"": NtpOutput.ShowNtpAssociations}

        ntp.maker.outputs[ShowNtpStatus] = \
            {"": {}}

        ntp.maker.outputs[ShowRunningConfigNtp] = \
            {"": {}}

        # Learn the feature
        ntp.learn()
                
        # Check no attribute not found
        with self.assertRaises(KeyError):
            ntp.info['clock_state']['system_status']['actual_freq']
            ntp.info['clock_state']['system_status']['clock_precision']
            ntp.info['clock_state']['system_status']['reference_time']
            ntp.info['clock_state']['system_status']['root_dispersion']


if __name__ == '__main__':
    unittest.main()