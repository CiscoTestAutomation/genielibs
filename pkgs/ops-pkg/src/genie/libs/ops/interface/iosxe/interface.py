''' 
Interface Genie Ops Object for IOSXE - CLI.
'''

import re

# super class
from genie.libs.ops.interface.interface import Interface as SuperInterface

# iosxe show_interface
from genie.libs.parser.iosxe.show_interface import ShowInterfaces, \
                                        ShowIpInterface,  \
                                        ShowIpv6Interface, \
                                        ShowInterfacesAccounting

from genie.libs.parser.iosxe.show_vrf import ShowVrf



class Interface(SuperInterface):
    '''Interface Genie Ops Object'''

    def learn(self, custom=None, interface=None, vrf=None, address_family=None):
        '''Learn Interface Ops'''
        ########################################################################
        #                               info
        ########################################################################
        # Global source
        src = '[(?P<interface>.*)]'
        dest = 'info[(?P<interface>.*)]'
        req_keys = ['[description]', '[type]', '[oper_status]',
                    '[phys_address]', '[port_speed]', '[mtu]',
                    '[enabled]', '[bandwidth]', '[flow_control]',
                    '[mac_address]', '[auto_negotiate]', '[port_channel]',
                    '[duplex_mode]', '[medium]', '[delay]']


        self.add_leaf(cmd=ShowVrf,
                      src='vrf[(?P<vrf>.*)][interfaces]',
                      dest='info[vrf][(?P<vrf>.*)][interfaces]', vrf=vrf)
        self.make()
        if vrf:
            for intf in self.info['vrf'][vrf]['interfaces']:
                for key in req_keys:
                    self.add_leaf(cmd=ShowInterfaces,
                                  src=src + '[{}]'.format(key),
                                  dest=dest + '[{}]'.format(key),
                                  interface=intf)
        else:
            for key in req_keys:
                self.add_leaf(cmd=ShowInterfaces,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key),
                              interface=interface)



        # make to write in cache
        self.make()

        # mapping vrf to interface from ShowVrf
        if interface:
            if hasattr(self, 'info') and 'vrf' in self.info:
                for vrf_entry in self.info['vrf']:
                    if 'interfaces' not in self.info['vrf'][vrf_entry]:
                        continue
                    for intf in self.info['vrf'][vrf_entry]['interfaces']:
                        if intf == interface:
                            if intf not in self.info:
                                self.info[intf] = {}
                            self.info[intf]['vrf'] = vrf_entry
                del (self.info['vrf'])
        else:
            if hasattr(self, 'info') and 'vrf' in self.info:
                for vrf_entry in self.info['vrf']:
                    if 'interfaces' not in self.info['vrf'][vrf_entry]:
                        continue
                    for intf in self.info['vrf'][vrf_entry]['interfaces']:
                        if intf not in self.info:
                            self.info[intf] = {}
                        self.info[intf]['vrf'] = vrf_entry
                del (self.info['vrf'])

        # make to write in cache
        self.make()

        # vrf_downstream not supported on iosxe

        # vlan_id access_vlan trunk_vlans
        # switchport_mode switchport_enable native_vlan
        # are only supported on c3850 platform

        # ======================================================================
        #                           counters
        # ======================================================================
        # keys are not supported on iosxe
        # 'in_unicast_pkts'
        # 'in_discards'
        # 'in_unknown_protos'
        # 'in_mac_control_frames'
        # 'in_oversize_frames'
        # 'in_jabber_frames'
        # 'in_fragment_frames'
        # 'in_8021q_frames'
        # 'out_unicast_pkts'
        # 'out_discard'
        # 'out_mac_control_frames'
        # 'out_8021q_frames'

        # Global source
        if vrf:
            for intf in self.info:
                src = '[(?P<interface>.*)][counters]'
                dest = 'info[(?P<interface>.*)][counters]'

                req_keys = ['in_pkts', 'in_octets', 'in_broadcast_pkts',
                            'in_multicast_pkts', 'in_errors',
                            'in_mac_pause_frames', 'out_mac_pause_frames',
                            'in_crc_errors', 'out_pkts', 'out_octets',
                            'out_broadcast_pkts', 'out_multicast_pkts',
                            'out_errors', 'last_clear']

                for key in req_keys:
                    self.add_leaf(cmd=ShowInterfaces,
                                  src=src + '[{}]'.format(key),
                                  dest=dest + '[{}]'.format(key),
                                  interface=intf)

                # Global source - counters | rate
                src = '[(?P<interface>.*)][counters][rate]'
                dest = 'info[(?P<interface>.*)][counters][rate]'

                req_keys = ['load_interval', 'in_rate', 'in_rate_pkts',
                            'out_rate', 'out_rate_pkts']
                for key in req_keys:
                    self.add_leaf(cmd=ShowInterfaces,
                                  src=src + '[{}]'.format(key),
                                  dest=dest + '[{}]'.format(key),
                                  interface=intf)

                # ======================================================================
                #                           encapsulation
                # ======================================================================

                # Global source
                src = '[(?P<interface>.*)][encapsulations]'
                dest = 'info[(?P<interface>.*)][encapsulation]'

                req_keys = ['encapsulation', 'first_dot1q', 'second_dot1q']

                for key in req_keys:
                    self.add_leaf(cmd=ShowInterfaces,
                                  src=src + '[{}]'.format(key),
                                  dest=dest + '[{}]'.format(key),
                                  interface=intf)

                # ======================================================================
                #                           accounting
                # ======================================================================

                # Global source
                src = '[(?P<interface>.*)]'
                dest = 'info[(?P<interface>.*)]'

                cmd = 'ShowInterfacesAccounting'
                if custom and cmd in custom.keys():
                    if 'intf' in custom[cmd].keys():
                        self.add_leaf(cmd=ShowInterfacesAccounting,
                                      src=src + '[accounting]',
                                      dest=dest + '[accounting]',
                                      interface=custom[cmd]['intf'])
                    else:
                        self.add_leaf(cmd=ShowInterfacesAccounting,
                                      src=src + '[accounting]',
                                      dest=dest + '[accounting]')

                self.add_leaf(cmd=ShowInterfacesAccounting,
                              src=src + '[accounting]',
                              dest=dest + '[accounting]',
                              interface=intf)

                # ======================================================================
                #                           ipv4
                # ======================================================================

                if not address_family or address_family.lower() == 'ipv4':
                    # Global source
                    src = '[(?P<interface>.*)][ipv4][(?P<ipv4>.*)]'
                    dest = 'info[(?P<interface>.*)][ipv4][(?P<ipv4>.*)]'

                    req_keys = ['ip', 'prefix_length', 'secondary', 'origin']
                    # custom
                    for key in req_keys:
                        self.add_leaf(cmd=ShowIpInterface,
                                      src=src + '[{}]'.format(key),
                                      dest=dest + '[{}]'.format(key), interface=intf)

                    # route_tag    --- This is not supported on IOSXE

                    # secondary_vrf   --- This is not supported on IOSXE

                    # unnumbered
                    self.add_leaf(cmd=ShowInterfaces,
                                  src='[(?P<interface>.*)][ipv4][unnumbered]',
                                  dest='info[(?P<interface>.*)][ipv4][unnumbered]',
                                  interface=intf)

                # ======================================================================
                #                           ipv6
                # ======================================================================

                # Global source
                if not address_family or address_family.lower() == 'ipv6':
                    src = '[(?P<interface>.*)][ipv6][(?P<ipv6>.*)]'
                    dest = 'info[(?P<interface>.*)][ipv6][(?P<ipv6>.*)]'
                    req_keys = ['ip', 'prefix_length', 'anycast', 'status',
                                'origin', 'autoconf', 'eui_64', 'enabled',
                                'unnumbered']

                    for key in req_keys:
                        self.add_leaf(cmd=ShowIpv6Interface,
                                      src=src + '[{}]'.format(key),
                                      dest=dest + '[{}]'.format(key), interface=intf)
        else:
            src = '[(?P<interface>.*)][counters]'
            dest = 'info[(?P<interface>.*)][counters]'

            req_keys = ['in_pkts', 'in_octets', 'in_broadcast_pkts',
                                'in_multicast_pkts', 'in_errors',
                                'in_mac_pause_frames', 'out_mac_pause_frames',
                                'in_crc_errors', 'out_pkts', 'out_octets',
                                'out_broadcast_pkts', 'out_multicast_pkts',
                                'out_errors', 'last_clear']


            for key in req_keys:
                self.add_leaf(cmd=ShowInterfaces,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key),
                              interface=interface)


            # Global source - counters | rate
            src = '[(?P<interface>.*)][counters][rate]'
            dest = 'info[(?P<interface>.*)][counters][rate]'

            req_keys = ['load_interval', 'in_rate', 'in_rate_pkts',
                        'out_rate', 'out_rate_pkts']
            for key in req_keys:
                self.add_leaf(cmd=ShowInterfaces,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key),
                              interface=interface)

            # ======================================================================
            #                           encapsulation
            # ======================================================================


            # Global source
            src = '[(?P<interface>.*)][encapsulations]'
            dest = 'info[(?P<interface>.*)][encapsulation]'

            req_keys = ['encapsulation', 'first_dot1q', 'second_dot1q']

            for key in req_keys:
                self.add_leaf(cmd=ShowInterfaces,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key),
                              interface=interface)

            # ======================================================================
            #                           accounting
            # ======================================================================

            # Global source
            src = '[(?P<interface>.*)]'
            dest = 'info[(?P<interface>.*)]'

            cmd = 'ShowInterfacesAccounting'
            if custom and cmd in custom.keys():
                if 'intf' in custom[cmd].keys():
                    self.add_leaf(cmd=ShowInterfacesAccounting,
                                  src=src + '[accounting]',
                                  dest=dest + '[accounting]',
                                  interface=custom[cmd]['intf'])
                else:
                    self.add_leaf(cmd=ShowInterfacesAccounting,
                                  src=src + '[accounting]',
                                  dest=dest + '[accounting]')

            self.add_leaf(cmd=ShowInterfacesAccounting,
                          src=src + '[accounting]',
                          dest=dest + '[accounting]',
                          interface=interface)


            # ======================================================================
            #                           ipv4
            # ======================================================================

            if not address_family or address_family.lower() == 'ipv4':
                # Global source
                src = '[(?P<interface>.*)][ipv4][(?P<ipv4>.*)]'
                dest = 'info[(?P<interface>.*)][ipv4][(?P<ipv4>.*)]'

                req_keys = ['ip', 'prefix_length', 'secondary', 'origin']
                # custom
                for key in req_keys:
                    self.add_leaf(cmd=ShowIpInterface,
                                  src=src + '[{}]'.format(key),
                                  dest=dest + '[{}]'.format(key), interface=interface)


                # route_tag    --- This is not supported on IOSXE

                # secondary_vrf   --- This is not supported on IOSXE

                # unnumbered
                self.add_leaf(cmd=ShowInterfaces,
                              src='[(?P<interface>.*)][ipv4][unnumbered]',
                              dest='info[(?P<interface>.*)][ipv4][unnumbered]',
                              interface=interface)

            # ======================================================================
            #                           ipv6
            # ======================================================================


            # Global source
            if not address_family or address_family.lower() == 'ipv6':
                src = '[(?P<interface>.*)][ipv6][(?P<ipv6>.*)]'
                dest = 'info[(?P<interface>.*)][ipv6][(?P<ipv6>.*)]'
                req_keys = ['ip', 'prefix_length', 'anycast', 'status',
                            'origin', 'autoconf', 'eui_64', 'enabled',
                            'unnumbered']

                for key in req_keys:
                    self.add_leaf(cmd=ShowIpv6Interface,
                                  src=src + '[{}]'.format(key),
                                  dest=dest + '[{}]'.format(key), interface=interface)

            # route_tag    --- This is not supported on IOSXE

        # make to write in cache
        self.make(final_call=True)

        # switchport_enable   -- default values
        if hasattr(self, 'info'):
            for intf in self.info:
                if 'switchport_enable' not in self.info[intf]:
                    self.info[intf]['switchport_enable'] = False
