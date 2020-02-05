# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.acl.iosxe.acl import Acl
from genie.libs.ops.acl.iosxe.tests.acl_output import AclOutput

# Parser
from genie.libs.parser.iosxe.show_acl import ShowAccessLists


class TestAcl(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
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

        # Learn the feature
        acl.learn()

        # Verify Ops was created successfully
        self.assertEqual(acl.info, AclOutput.Acl_info)

        # Check Selected Attributes
        self.assertEqual(acl.info['acls']['acl_name']['name'], 'acl_name')
        # info - ipv4_acl
        self.assertEqual(acl.info['acls']['ipv4_acl']['aces']['20']\
            ['actions']['forwarding'], 'permit')

    def test_empty_output(self):
        self.maxDiff = None
        acl = Acl(device=self.device)

        acl.maker.outputs[ShowAccessLists] = \
            {'': {}}

        # Learn the feature
        acl.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            acl.info['acls']['acl_name']['name']

    def test_incomplete_output(self):
        self.maxDiff = None
        
        acl = Acl(device=self.device)
        # Get outputs
        acl.maker.outputs[ShowAccessLists] = \
            {'': AclOutput.ShowAccessLists}

        # delete keys from input
        del(AclOutput.ShowAccessLists['acl_name']['name'])

        # Learn the feature
        acl.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(AclOutput.Acl_info)
        del(expect_dict['acls']['acl_name']['name'])
                
        # Verify Ops was created successfully
        self.assertEqual(acl.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
