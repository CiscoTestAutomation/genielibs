
# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.lisp.iosxe.lisp import Lisp
from genie.libs.ops.lisp.iosxe.tests.lisp_output import LispOutput

# iosxe show_lisp
from genie.libs.parser.iosxe.show_lisp import ShowLispSession,\
                                              ShowLispPlatform,\
                                              ShowLispExtranet,\
                                              ShowLispDynamicEidDetail,\
                                              ShowLispService,\
                                              ShowLispServiceMapCache,\
                                              ShowLispServiceRlocMembers,\
                                              ShowLispServiceSmr,\
                                              ShowLispServiceSummary,\
                                              ShowLispServiceDatabase,\
                                              ShowLispServiceServerSummary,\
                                              ShowLispServiceServerDetailInternal,\
                                              ShowLispServiceStatistics


# Set values
output = {}

# 'show lisp all service <service>'
output['show lisp all service ipv4'] = LispOutput.ShowLispServiceIpv4
output['show lisp all service ipv6'] = LispOutput.ShowLispServiceIpv6
output['show lisp all service ethernet'] = LispOutput.ShowLispServiceEthernet

# 'show lisp all service <service> summary'
output['show lisp all service ipv4 summary'] = LispOutput.ShowLispServiceIpv4Summary
output['show lisp all service ipv6 summary'] = LispOutput.ShowLispServiceIpv6Summary
output['show lisp all service ethernet summary'] = LispOutput.ShowLispServiceEthernetSummary

# 'show lisp all instance-id <instance_id> <service>'
output['show lisp all instance-id 101 ipv4'] = LispOutput.ShowLispInstance101ServiceIpv4
output['show lisp all instance-id 101 ipv6'] = LispOutput.ShowLispInstance101ServiceIpv6
output['show lisp all instance-id 101 ethernet'] = LispOutput.ShowLispInstance101ServiceEthernet

# 'show lisp all instance-id <instance_id> <service> server detail internal'
output['show lisp all instance-id 101 ipv4 server detail internal'] = LispOutput.ShowLispInstance101Ipv4ServerDetailInternal
output['show lisp all instance-id 101 ipv6 server detail internal'] = LispOutput.ShowLispInstance101Ipv6ServerDetailInternal
output['show lisp all instance-id 101 ethernet server detail internal'] = LispOutput.ShowLispInstance101EthernetServerDetailInternal

# 'show lisp all extranet <extranet> instance-id <instance_id>'
output['show lisp all extranet ext1 instance-id 101'] = LispOutput.ShowLispExtranet101

# 'show lisp all instance-id <instance_id> <service> statistics'
output['show lisp all instance-id 101 ipv4 statistics'] = LispOutput.ShowLispInstance101Ipv4Stats
output['show lisp all instance-id 101 ipv6 statistics'] = LispOutput.ShowLispInstance101Ipv6Stats
output['show lisp all instance-id 101 ethernet statistics'] = LispOutput.ShowLispInstance101EthernetStats

# 'show lisp all instance-id <instance_id> <service> server summary'
output['show lisp all instance-id 101 ipv4 server summary'] = LispOutput.ShowLispInstance101Ipv4ServerSummary
output['show lisp all instance-id 101 ipv6 server summary'] = LispOutput.ShowLispInstance101Ipv6ServerSummary
output['show lisp all instance-id 101 ethernet server summary'] = LispOutput.ShowLispInstance101EthernetServerSummary

# 'show lisp all instance-id <instance-d> <service> map-cache'
output['show lisp all instance-id 101 ipv4 map-cache'] = LispOutput.ShowLispInstance101Ipv4MapCache
output['show lisp all instance-id 101 ipv6 map-cache'] = LispOutput.ShowLispInstance101Ipv6MapCache
output['show lisp all instance-id 101 ethernet map-cache'] = LispOutput.ShowLispInstance101EthernetMapCache

# 'show lisp all instance-id <instance_id> <service> dabatase'
output['show lisp all instance-id 101 ipv4 database'] = LispOutput.ShowLispInstance101Ipv4Database
output['show lisp all instance-id 101 ipv6 database'] = LispOutput.ShowLispInstance101Ipv6Database
output['show lisp all instance-id 101 ethernet database'] = LispOutput.ShowLispInstance101EthernetDatabase



def mapper(key):
    return output[key]


def empty_mapper(key):
    return ''


def incomplete_mapper(key):
    if key == 'show lisp all instance-id 101 ipv4':
        return ''
    else:
        return output[key]


class test_lisp(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        # Give the device as a connection type
        # This is done in order to call the parser on the output provided
        self.device.connectionmgr.connections['cli'] = self.device


    def test_complete_output(self):
        self.maxDiff = None
        lisp = Lisp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        lisp.learn()

        # Verify Ops was created successfully
        self.assertEqual(lisp.info, LispOutput.LispInfo)


    def test_selective_attribute(self):
        self.maxDiff = None
        lisp = Lisp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = mapper

        # Learn the feature
        lisp.learn()

        # Check selective attribute
        self.assertEqual('10.166.13.13', lisp.info['lisp_router_instances'][0]\
                                        ['service']['ipv4']['etr']\
                                        ['mapping_servers']['10.166.13.13']\
                                        ['ms_address'])


    def test_empty_output(self):
        self.maxDiff = None
        lisp = Lisp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = empty_mapper

        # Learn the feature
        lisp.learn()

        # Verify attribute is missing
        with self.assertRaises(AttributeError):
            lisp.info['lisp_router_instances']


    def test_missing_attributes(self):
        self.maxDiff = None
        lisp = Lisp(device=self.device)

        # Return outputs above as inputs to parser when called
        self.device.execute = Mock()
        self.device.execute.side_effect = incomplete_mapper

        # Learn the feature
        lisp.learn()

        # Verify key not created due to ouput missing
        with self.assertRaises(KeyError):
            ms_address = lisp.info['lisp_router_instances'][0]\
                                        ['service']['ipv4']['etr']\
                                        ['mapping_servers']['10.166.13.13']\
                                        ['ms_address']


if __name__ == '__main__':
    unittest.main()
