'''
Platform Genie Ops Object for IOSXR.
'''
import logging

# super class
from genie.libs.ops.management.management import Management as SuperManagement

logger = logging.getLogger(__name__)


class Management(SuperManagement):
    '''Management Genie Ops Object'''

    def learn(self):

        self.add_leaf(cmd='show ipv4 virtual address status',
                      src='[virtual_address][virtual_ip]',
                      dest='info[management][ipv4][virtual_address]')

        self.add_leaf(cmd='show ipv4 virtual address status',
                      src='[virtual_address][active_interface_name]',
                      dest='info[management][interface]')

        self.add_leaf(cmd='show ipv4 virtual address status',
                      src='[virtual_address][vrf_name]',
                      dest='info[management][vrf]')

        self.make()

        if hasattr(self, 'info') and self.info:

            iface = self.info['management']['interface']

            self.add_leaf(cmd=f'show route ipv4 next-hop {iface}',
                        src='[vrf][default][address_family][ipv4][routes]'
                            '[(?P<route>.*)][next_hop][next_hop_list][(?P<idx>).*][next_hop]',
                        dest='info[routes][ipv4][(?P<route>.*)][next_hop]',
                        next_hop=iface
                        )

            self.add_leaf(cmd=f'show route ipv4 next-hop {iface}',
                        src='[vrf][default][address_family][ipv4][routes]'
                            '[(?P<route>.*)][source_protocol]',
                        dest='info[routes][ipv4][(?P<route>.*)][source_protocol]',
                        next_hop=iface
                        )

        # Make Ops object
        self.make(final_call=True)
