''' 
HSRP Genie Ops Object for NXOS.
'''

from genie.libs.ops.hsrp.hsrp import Hsrp as SuperHsrp
from genie.ops.base import Context

# Parser
from genie.libs.parser.nxos.show_hsrp import ShowHsrpSummary, ShowHsrpAll, ShowHsrpDelay

class Hsrp(SuperHsrp):
    '''HSRP Genie Ops Object'''

    def learn(self):
        '''Learn HSRP Ops'''

        ########################################################################
        #                               info
        ########################################################################

        # enabled N/A

        # interface
        #  'address_family'
        #   address_family
        #    'version'
        #     version
        #      'groups'
        #       group_number
        hsrp_src = '[(?P<interface>.*)][address_family]'\
                   '[(?P<address_family>.*)][version][(?P<version>.*)][groups]'\
                   '[(?P<groups>.*)]'
        hsrp_dest = 'info' + hsrp_src

        # bfd_address N/A
        # bfd_interface_name N/A
        # tracked_interface N/A
        # tracked_intf_priority_decrement N/A

        # tracked_object
        # tracked_object_priority_decrement
        for key in ['object_name', 'priority_decrement']:
            self.add_leaf(cmd=ShowHsrpAll,
                          src=hsrp_src+'[tracked_objects]'
                              '[(?P<tracked_objects>.*)][{key}]'\
                              .format(key=key),
                          dest=hsrp_dest+'[tracked_objects]'
                               '[(?P<tracked_objects>.*)][{key}]'\
                               .format(key=key))

        # hello_msec_flag
        # hello_msec
        # hello_sec
        # hold_msec_flag
        # hold_msec
        # hold_sec
        for key in ['hello_msec_flag', 'hello_msec', 'hello_sec',\
         'hold_msec_flag', 'hold_msec', 'hold_sec']:
            self.add_leaf(cmd=ShowHsrpAll,
                          src=hsrp_src+'[timers][{key}]'.format(key=key),
                          dest=hsrp_dest+'[timers][{key}]'.format(key=key))

        # virtual_ip_learn
        # primary_ipv4_address
        for key in ['virtual_ip_learn', 'address']:
            self.add_leaf(cmd=ShowHsrpAll,
                          src=hsrp_src+'[primary_ipv4_address]'
                              '[{key}]'.format(key=key),
                          dest=hsrp_dest+'[primary_ipv4_address]'
                               '[{key}]]'.format(key=key))

        # secondary_ipv4_addres
        self.add_leaf(cmd=ShowHsrpAll,
                      src=hsrp_src+'[secondary_ipv4_addresses]'
                          '[(?P<secondary_ipv4_addresses>.*)][address]',
                      dest=hsrp_dest+'[secondary_ipv4_addresses]'
                           '[(?P<secondary_ipv4_addresses>.*)][address]')

        # link_local_ipv6_address
        # hsrp_linklocal
        for key in ['address', 'auto_configure']:
            self.add_leaf(cmd=ShowHsrpAll,
                          src=hsrp_src+'[link_local_ipv6_address]'
                              '[{key}]'.format(key=key),
                          dest=hsrp_dest+'[link_local_ipv6_address]'
                               '[{key}]'.format(key=key))

        # global_ipv6_address
        self.add_leaf(cmd=ShowHsrpAll,
                      src=hsrp_src+'[global_ipv6_address]'
                          '[(?P<global_ipv6_address>.*)][address]'
                          '[(?P<address>.*)]',
                      dest=hsrp_dest+'[global_ipv6_address]'
                           '[(?P<global_ipv6_address>.*)][address]'
                           '[(?P<address>.*)]')

        # authentication
        # priority
        # preempt
        # session_name
        # virtual_mac_address
        # group_number
        # active_ip_address
        # active_ipv6_address
        # active_mac_address N/A
        # standby_ip_address
        # standby_ipv6_address
        # standby_mac_address N/A
        # hsrp_router_state
        # active_router
        # standby_router
        for key in ['authentication', 'priority', 'preempt', 'session_name',\
            'virtual_mac_address', 'group_number', 'active_ip_address',\
            'active_ipv6_address', 'standby_ip_address', \
            'standby_ipv6_address','hsrp_router_state', 'active_router',\
            'standby_router']:
            self.add_leaf(cmd=ShowHsrpAll,
                          src=hsrp_src+'[{key}]'.format(key=key),
                          dest=hsrp_dest+'[{key}]'.format(key=key))

        # active_transitions N/A
        # standby_transitions N/A
        # speak_transitions N/A
        # listen_transitions N/A
        # learn_transitions N/A
        # init_transitions N/A
        # hello_packets_sent N/A
        # resign_packets_sent N/A
        # coup_packets_sent N/A
        # hello_packets_received N/A
        # resign_packets_received N/A
        # coup_packets_received N/A
        # auth_fail_received N/A
        # invalid_timer_received N/A
        # mismatch_virtual_ip_address_received N/A

        # interface
        #  'address_family'
        #   address_family
        #    'version'
        #     version
        #      'slave_groups'
        #       slave_group_number
        hsrp_src = '[(?P<interface>.*)][address_family]'\
                   '[(?P<address_family>.*)][version][(?P<version>.*)]'\
                   '[slave_groups][(?P<slave_groups>.*)]'
        hsrp_dest = 'info' + hsrp_src

        # secondary_ipv4_addres
        self.add_leaf(cmd=ShowHsrpAll,
                      src=hsrp_src+'[secondary_ipv4_addresses]'
                          '[(?P<secondary_ipv4_addresses>.*)][address]',
                      dest=hsrp_dest+'[secondary_ipv4_addresses]'
                           '[(?P<secondary_ipv4_addresses>.*)][address]')

        # primary_ipv4_address
        self.add_leaf(cmd=ShowHsrpAll,
                      src=hsrp_src+'[primary_ipv4_address',
                      dest=hsrp_dest+'[primary_ipv4_address]')

        # link_local_ipv6_address
        # hsrp_linklocal
        for key in ['address', 'auto_configure']:
            self.add_leaf(cmd=ShowHsrpAll,
                          src=hsrp_src+'[link_local_ipv6_address]'
                              '[{key}]'.format(key=key),
                          dest=hsrp_dest+'[link_local_ipv6_address]'
                               '[{key}]'.format(key=key))

        # global_ipv6_address
        self.add_leaf(cmd=ShowHsrpAll,
                      src=hsrp_src+'[global_ipv6_address]'
                          '[(?P<global_ipv6_address>.*)][address]'
                          '[(?P<address>.*)]',
                      dest=hsrp_dest+'[global_ipv6_address]'
                           '[(?P<global_ipv6_address>.*)][address]'
                           '[(?P<address>.*)]')

        # follow
        # virtual_mac_address
        # slave_group_number
        for key in ['follow', 'virtual_mac_address', 'slave_group_number']:
            self.add_leaf(cmd=ShowHsrpAll,
                          src=hsrp_src+'[{key}]'.format(key=key),
                          dest=hsrp_dest+'[{key}]'.format(key=key))

        # interface
        hsrp_src = '[(?P<interface>.*)]'
        hsrp_dest = 'info' + hsrp_src

        # bfd_enabled
        # bfd_detection_multiplier N/A
        # bfd_interval N/A
        self.add_leaf(cmd=ShowHsrpAll,
                      src=hsrp_src+'[bfd][enabled]',
                      dest=hsrp_dest+'[bfd][enabled]')

        # minimum_delay
        # reload_delay
        for key in ['minimum_delay', 'reload_delay']:
            self.add_leaf(cmd=ShowHsrpDelay,
                          src=hsrp_src+'[delay][{key}]'.format(key=key),
                          dest=hsrp_dest+'[delay][{key}]'.format(key=key))

        # mac_refresh N/A
        # use_bia
        # redirects_disable
        # interface
        for key in ['use_bia', 'redirects_disable', 'interface']:
            self.add_leaf(cmd=ShowHsrpAll,
                          src=hsrp_src+'[{key}]'.format(key=key),
                          dest=hsrp_dest+'[{key}]'.format(key=key))

        # state_change_disable N/A

        self.make(final_call=True)

# vim: ft=python et sw=4
