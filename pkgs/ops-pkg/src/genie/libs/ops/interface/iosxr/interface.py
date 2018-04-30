''' 
Interface Genie Ops Object for IOSXR - CLI.
'''
# python
import re

# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# iosxr show_interface
from genie.libs.parser.iosxr.show_interface import ShowInterfacesDetail, ShowEthernetTags, \
                                 ShowIpv4VrfAllInterface, ShowIpv6VrfAllInterface

from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail


class Interface(Base):
    '''Interface Genie Ops Object'''

    def learn(self):
        '''Learn Interface Ops'''
        
        ########################################################################
        #                               info
        ########################################################################
        # Global source
        src = '[(?P<interface>.*)]'
        dest = 'info[(?P<interface>.*)]'
        req_keys_path = {'[description]': '[description]',
                        '[types]': '[type]',
                        '[oper_status]': '[oper_status]',
                        '[phys_address]': '[phys_address]',
                        '[port_speed]': '[port_speed]',
                        '[mtu]': '[mtu]',
                        '[enabled]': '[enabled]',
                        '[mac_address]': '[mac_address]',
                        '[auto_negotiate]': '[auto_negotiate]',
                        '[duplex_mode]': '[duplex_mode]',
                        '[bandwidth]': '[bandwidth]',
                   }

        for src_key_path, dest_key_path in req_keys_path.items():
            self.add_leaf(cmd=ShowInterfacesDetail,
                          src=src + src_key_path,
                          dest=dest + dest_key_path)

        # vrf
        self.add_leaf(cmd=ShowVrfAllDetail,
                      src='[(?P<vrf>.*)][interfaces]',
                      dest='info[vrf][(?P<vrf>.*)][interfaces]')


        # make to write in cache
        self.make()
        
        # mapping vrf to interface from ShowVrfAllDetail
        if hasattr(self, 'info') and 'vrf' in self.info:
            for vrf in self.info['vrf']:
                if 'interfaces' not in self.info['vrf'][vrf]:
                    continue
                for intf in self.info['vrf'][vrf]['interfaces']:
                    if intf not in self.info:
                        self.info[intf] = {}
                    self.info[intf]['vrf'] = vrf
            del(self.info['vrf'])

        # vlan_id
        self.add_leaf(cmd=ShowEthernetTags,
                      src=src + '[vlan_id]',
                      dest=dest + '[vlan_id]')

        # ======================================================================
        #                           flow_control
        # ======================================================================

        # flow_control
        self.add_leaf(cmd=ShowInterfacesDetail,
                      src=src + '[flow_control]',
                      dest=dest + '[flow_control]')


        # ======================================================================
        #                           counters
        # ======================================================================
        # Global source
        src = '[(?P<interface>.*)][counters]'
        dest = 'info[(?P<interface>.*)][counters]'

        req_keys = ['in_pkts', 'in_octets', 'out_discard',
                    'in_broadcast_pkts', 'in_multicast_pkts',
                    'in_discards', 'in_errors', 'out_octets',
                    'in_crc_errors', 'out_pkts',
                    'out_broadcast_pkts', 'out_multicast_pkts',
                    'out_errors', 'last_clear']

        for key in req_keys:
            self.add_leaf(cmd=ShowInterfacesDetail,
                          src=src + '[{}]'.format(key),
                          dest=dest + '[{}]'.format(key))


        # Global source - counters | rate
        src = '[(?P<interface>.*)][counters][rate]'
        dest = 'info[(?P<interface>.*)][counters][rate]'        

        req_keys = ['load_interval', 'in_rate', 'in_rate_pkts',
                    'out_rate', 'out_rate_pkts']

        for key in req_keys:
            self.add_leaf(cmd=ShowInterfacesDetail,
                          src=src + '[{}]'.format(key),
                          dest=dest + '[{}]'.format(key))

        # IOSXR NONE supported keys from general ops
        # in_8021q_frames - N/A
        # in_fragment_frames - N/A
        # in_jabber_frames - N/A
        # in_mac_control_frames - N/A
        # in_mac_pause_frames - N/A
        # in_unicast_pkts - N/A
        # in_oversize_frames - N/A
        # in_unknown_protos - N/A
        # ipv6_origin - N/A
        # ipv6_preferred_lifetime - N/A
        # ipv6_valid_lifetime - N/A
        # last_change - N/A
        # origin - N/A
        # medium - N/A
        # out_8021q_frames - N/A
        # out_mac_control_frames - N/A
        # out_mac_pause_frames - N/A
        # out_unicast_pkts - N/A
        # vrf_downstream - N/A in xr
        # access_vlan- N/A in XR
        # delay - N/A in XR
        # secondary_vrf - N/A in xr
        # switchport_mode - N/A in xr
        # trunk_vlans - N/A in xr
        # link_status - N/A in xr
        # ipv6_unnumbered_intf_ref - N/A in xr
        # ipv6_anycast - N/A in xr

        # ======================================================================
        #                           encapsulation
        # ======================================================================
        

        # Global source
        src = '[(?P<interface>.*)][encapsulations]'
        dest = 'info[(?P<interface>.*)][encapsulation]'

        req_keys = ['encapsulation', 'first_dot1q',
                    'second_dot1q', 'native_vlan']

        for key in req_keys:
            self.add_leaf(cmd=ShowInterfacesDetail,
                          src=src + '[{}]'.format(key),
                          dest=dest + '[{}]'.format(key))

        # ======================================================================
        #                           ipv4
        # ======================================================================
        

        # Global source
        src = '[(?P<interface>.*)][ipv4][(?P<ipv4>.*)]'
        dest = 'info[(?P<interface>.*)][ipv4][(?P<ipv4>.*)]'

        req_keys = ['ip', 'prefix_length', 'secondary', 'route_tag']

        for key in req_keys:
            self.add_leaf(cmd=ShowIpv4VrfAllInterface,
                          src=src + '[{}]'.format(key),
                          dest=dest + '[{}]'.format(key))
        
        # unnumbered
        self.add_leaf(cmd=ShowIpv4VrfAllInterface,
                      src='[(?P<interface>.*)][ipv4][unnumbered][unnumbered_intf_ref]',
                      dest='info[(?P<interface>.*)][ipv4][unnumbered][unnumbered_intf_ref]')


        # ======================================================================
        #                           ipv6
        # ======================================================================
        

        # Global source
        src = '[(?P<interface>.*)][ipv6][(?P<ipv6>.*)]'
        dest = 'info[(?P<interface>.*)][ipv6][(?P<ipv6>.*)]'

        req_keys_path = {'[ipv6]': '[ip]',
                        '[ipv6_prefix_length]': '[prefix_length]',
                        '[ipv6_status]': '[status]',
                        '[ipv6_eui64]': '[eui64]',
                        '[ipv6_route_tag]': '[route_tag]',
                   }

        for src_key_path, dest_key_path in req_keys_path.items():
            self.add_leaf(cmd=ShowIpv6VrfAllInterface,
                          src=src + src_key_path,
                          dest=dest + dest_key_path)
        
        # enabled
        self.add_leaf(cmd=ShowIpv6VrfAllInterface,
                      src='[(?P<interface>.*)][ipv6_enabled]',
                      dest='info[(?P<interface>.*)][ipv6][enabled]')

        # make to write in cache
        self.make()

        
