# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.acl.nxos.acl import Acl
from genie.libs.ops.acl.nxos.tests.acl_output import AclOutput

# Parser
from genie.libs.parser.nxos.show_acl import ShowAccessLists, ShowAccessListsSummary


class TestAcl(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_empty_output(self):
        self.maxDiff = None
        acl = Acl(device=self.device)

        acl.maker.outputs[ShowAccessLists] = \
            {'': {}}
        acl.maker.outputs[ShowAccessListsSummary] = \
            {'': {}}

        # Learn the feature
        acl.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            acl.info['acls']

    def test_complete_output(self):
        acl = Acl(device=self.device)
        # Get outputs
        acl.maker.outputs[ShowAccessLists] = \
            {'': AclOutput.ShowAccessLists}

        acl.maker.outputs[ShowAccessListsSummary] = \
            {'': AclOutput.ShowAccessListsSummary}
        # Learn the feature
        acl.learn()

        # Verify Ops was created successfully
        self.assertEqual(acl.info, AclOutput.aclOutput)

        # Check Selected Attributes
        self.assertEqual(acl.info['acls']['acl_name']['name'], 'acl_name')
        # info - ipv4_acl
        self.assertEqual(acl.info['acls']['test22']['aces']['30'] \
                                ['actions']['forwarding'], 'drop')

    def test_incomplete_output(self):
        self.maxDiff = None

        acl = Acl(device=self.device)
        # Get outputs
        acl.maker.outputs[ShowAccessLists] = \
            {'': AclOutput.ShowAccessLists}

        acl.maker.outputs[ShowAccessListsSummary] = \
            {'': AclOutput.ShowAccessListsSummary}

        # delete keys from input
        del (AclOutput.ShowAccessLists['acl_name']['name'])

        # Learn the feature
        acl.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(AclOutput.aclOutput)
        del (expect_dict['acls']['acl_name']['name'])

        # Verify Ops was created successfully
        self.assertEqual(acl.info, expect_dict)


if __name__ == '__main__':
    unittest.main()