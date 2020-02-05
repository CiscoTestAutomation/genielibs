# Python
import unittest
from copy import deepcopy
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.acl.iosxr.acl import Acl
from genie.libs.ops.acl.iosxr.tests.acl_output import AclOutput

# Parser
from genie.libs.parser.iosxr.show_acl import ShowAclAfiAll, \
                                        ShowAclEthernetServices

class test_acl(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device

    def test_complete_output(self):
        acl = Acl(device=self.device)
        # Get outputs
        acl.maker.outputs[ShowAclAfiAll] = \
            {'': AclOutput.ShowAclAfiAll}

        acl.maker.outputs[ShowAclEthernetServices] = \
            {'': AclOutput.ShowAclEthernetServices}
        # Learn the feature
        acl.learn()
        # Verify Ops was created successfully
        self.assertEqual(acl.info, AclOutput.aclOutput)
        
        # Check Selected Attributes
        self.assertEqual(acl.info['acls']['acl_name']['name'], 'acl_name')
        # info - ipv4_acl
        self.assertEqual(acl.info['acls']['test22']['aces'][30]\
            ['actions']['forwarding'], 'drop')


    def test_empty_output(self):
        self.maxDiff = None
        acl = Acl(device=self.device)

        acl.maker.outputs[ShowAclAfiAll] = \
            {'': {}}

        acl.maker.outputs[ShowAclEthernetServices] = \
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
        acl.maker.outputs[ShowAclAfiAll] = \
            {'': AclOutput.ShowAclAfiAll}

        acl.maker.outputs[ShowAclEthernetServices] = \
            {'': AclOutput.ShowAclEthernetServices}
        # delete keys from input
        del(AclOutput.ShowAclAfiAll['acl_name']['name'])
        del(AclOutput.ShowAclEthernetServices['eth_acl']['name'])
        # Learn the feature
        acl.learn()

        # Delete missing specific attribute values
        expect_dict = deepcopy(AclOutput.aclOutput)
        del(expect_dict['acls']['acl_name']['name'])
        del(expect_dict['acls']['eth_acl']['name'])     
        # Verify Ops was created successfully
        self.assertEqual(acl.info, expect_dict)


if __name__ == '__main__':
    unittest.main()
