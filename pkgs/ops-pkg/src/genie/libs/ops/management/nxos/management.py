'''
Management Genie Ops Object for NXOS.
'''
import logging

# super class
from genie.libs.ops.management.management import Management as SuperManagement

logger = logging.getLogger(__name__)


class Management(SuperManagement):
    '''Management Genie Ops Object'''

    def learn(self):

        self.add_leaf(cmd='show ip route',
                      src='vrf[management][address_family][ipv4][routes][(?P<route>.*)/32][next_hop][next_hop_list][(?P<idx>.*)][next_hop]',
                      dest='info[management][ipv4_address]',
                      vrf='management')

        self.add_leaf(cmd='show ip route',
                      src='vrf[management][address_family][ipv4][routes][0.0.0.0/0][next_hop][next_hop_list][(?P<idx>.*)][next_hop]',
                      dest='info[management][ipv4_gateway]',
                      vrf='management')

        self.add_leaf(cmd='show ip route',
                      src='vrf[management][address_family][ipv4][routes][(?P<route>.*)][next_hop][next_hop_list][(?P<idx>.*)][next_hop]',
                      dest='info[management][ipv4][routes][(?P<route>.*)][next_hop]',
                      vrf='management')

        self.add_leaf(cmd='show ip route',
                      src='vrf[management][address_family][ipv4][routes][(?P<route>.*)][next_hop][next_hop_list][(?P<idx>.*)][outgoing_interface]',
                      dest='info[management][ipv4][routes][(?P<route>.*)][outgoing_interface]',
                      vrf='management')

        self.add_leaf(cmd='show ip route',
                      src='vrf[management][address_family][ipv4][routes][(?P<route>.*)][source_protocol]',
                      dest='info[management][ipv4][routes][(?P<route>.*)][source_protocol]',
                      vrf='management')

        self.make(final_call=True)

        self.info['management']['interface'] = 'mgmt0'
        self.info['management']['vrf'] = 'management'