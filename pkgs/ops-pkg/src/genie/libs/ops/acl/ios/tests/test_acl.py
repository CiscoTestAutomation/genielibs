# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.acl.ios.acl import Acl
from genie.libs.ops.acl.ios.tests.acl_output import AclOutput

# Parser
from genie.libs.parser.ios.show_acl import ShowAccessLists

outputs = {}
outputs['show access-lists'] = AclOutput.ShowAccessLists

def mapper(key):
    return outputs[key]

class TestAcl(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.custom['abstraction'] = {'order': ['os']}
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        self.maxDiff = None
        acl = Acl(device=self.device)
        # Get outputs
        acl.maker.outputs[ShowAccessLists] = \
            {'': AclOutput.ShowAccessLists}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper
        # Learn the feature
        acl.learn()

        # Verify Ops was created successfully
        self.assertDictEqual(acl.info, AclOutput.Acl_info)

        # Check Selected Attributes
        self.assertEqual(acl.info['acls']['101']['name'], '101')
        # info - ipv4_acl
        self.assertEqual(acl.info['acls']['101']['aces']['20']\
            ['actions']['forwarding'], 'permit')

    def test_empty_output(self):
        self.maxDiff = None
        acl = Acl(device=self.device)

        acl.maker.outputs[ShowAccessLists] = \
            {'': {}}

        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        acl.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            acl.info['acls']['101']['name']

    def test_incomplete_output(self):
        self.maxDiff = None

        acl = Acl(device=self.device)
        # Get outputs
        acl.maker.outputs[ShowAccessLists] = \
            {'': AclOutput.ShowAccessLists}

        # delete keys from input
        del(AclOutput.ShowAccessLists['101']['name'])

        # Learn the feature
        acl.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(AclOutput.Acl_info)
        del(expect_dict['acls']['101']['name'])

        # Verify Ops was created successfully
        self.assertEqual(acl.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
