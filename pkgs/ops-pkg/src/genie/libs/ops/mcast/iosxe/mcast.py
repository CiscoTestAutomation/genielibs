''' 
MCAST Genie Ops Object for IOSXE - CLI.
'''
# super class
from genie.libs.ops.mcast.mcast import Mcast as SuperMacst

# iosxe show_rpf
from genie.libs.parser.iosxe.show_rpf import ShowIpv6Rpf

# iosxe show_pim
from genie.libs.parser.iosxe.show_pim import ShowIpv6PimInterface

# iosxe show_vrf
from genie.libs.parser.iosxe.show_vrf import ShowVrfDetail


class Mcast(SuperMacst):
    '''Mcast Genie Ops Object'''

    def get_vrfs(self, item):
        if isinstance(item, dict):
            return list(item.keys())

    def learn(self):
        '''Learn Mcast Ops'''

        # get vrf list        
        self.add_leaf(cmd=ShowVrfDetail,
                      src='',
                      dest='list_of_vrfs',
                      action=self.get_vrfs)

        self.make()

        vrf_list = ['default']
        try:
            vrf_list.extend(self.list_of_vrfs)
        except:
            pass
        else:            
            # delete the list_of_vrfs in the info table
            del self.list_of_vrfs

        # loop for vrfs
        for vrf in sorted(vrf_list):

            # skip the vrf when it is mgmt-vrf
            if vrf == 'Mgmt-vrf':
                continue

            # create kwargs
            vrf_name = '' if vrf == 'default' else vrf
                

            ########################################################################
            #                                 info
            ########################################################################

            # enable - ipv4
            self.add_leaf(cmd='show ip multicast vrf {vrf}'.format(vrf=vrf),
                          src='[vrf][(?P<vrf>.*)][enable]',
                          dest='info[vrf][(?P<vrf>.*)][address_family][ipv4][enable]',
                          vrf=vrf_name)

            # multipath - ipv4
            self.add_leaf(cmd='show ip multicast vrf {vrf}'.format(vrf=vrf),
                          src='[vrf][(?P<vrf>.*)][multipath]',
                          dest='info[vrf][(?P<vrf>.*)][address_family][ipv4][multipath]',
                          vrf=vrf_name)

            # enable - ipv6
            self.add_leaf(cmd=ShowIpv6PimInterface,
                          src='[vrf][(?P<vrf>.*)][interface][(?P<interface>.*)][pim_enabled]',
                          dest='info[vrf][(?P<vrf>.*)][interface][(?P<interface>.*)][pim_enabled]',
                          vrf=vrf_name)
     

            # multipath - ipv6 from show run

            # ipv4 - neighbor_address, admin_distance
            info_src = '[vrf][(?P<vrf>.*)][mroute][(?P<mroute>.*)][path][(?P<path>.*)]'
            info_dest = 'info[vrf][(?P<vrf>.*)][address_family][ipv4]'\
                        '[mroute][(?P<mroute>.*)][path][(?P<path>.*)]'

            for key in ['neighbor_address', 'admin_distance']:
                self.add_leaf(cmd='show ip mroute vrf {vrf} static'.format(vrf=vrf),
                              src=info_src+'[{key}]'.format(key=key),
                              dest=info_dest+'[{key}]'.format(key=key),
                              vrf=vrf_name)

            ########################################################################
            #                               table
            ########################################################################

            tbl_src = '[vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)]'\
                      '[multicast_group][(?P<mcast_group>.*)][source_address][(?P<source_address>.*)]'
            tbl_dest = 'table' + tbl_src

            # flags, uptime, expire, rp
            # incoming_interface_list
            # outgoing_interface_list
            for key in ['flags', 'uptime', 'expire', 'rp', 'rpf_nbr',
                        'incoming_interface_list', 'outgoing_interface_list']:

                # ipv4 & ipv6
                for cmd in ['show ip mroute', 'show ipv6 mroute']:
                    self.add_leaf(cmd=cmd,
                                  src=tbl_src+'[{key}]'.format(key=key),
                                  dest=tbl_dest+'[{key}]'.format(key=key),
                                  vrf=vrf_name)

            self.make()

            try:
                ipv6_mroute_list = self.table['vrf'][vrf]['address_family']['ipv6']['multicast_group'].keys()
            except:
                ipv6_mroute_list = []

            # ipv6 - neighbor_address, interface_name, admin_distance
            info_src = '[vrf][(?P<vrf>.*)][path][(?P<path>.*)]'
            for mroute in ipv6_mroute_list:
                info_dest = 'info[vrf][(?P<vrf>.*)][address_family][ipv6]'\
                            '[mroute][{mroute}][path][(?P<path>.*)]'.format(mroute=mroute)

                for key in ['neighbor_address', 'interface_name', 'admin_distance']:
                    self.add_leaf(cmd=ShowIpv6Rpf,
                                  src=info_src+'[{key}]'.format(key=key),
                                  dest=info_dest+'[{key}]'.format(key=key),
                                  vrf=vrf_name, mroute=mroute)
            self.make(final_call=True)

            # define attribute enable - ipv6
            # the commadn is Show ipv6 rpf, so this is only for ipv6 enabled
            try:
                for intf in self.info['vrf'][vrf]['interface']:
                    if self.info['vrf'][vrf]['interface'][intf]['pim_enabled']:
                        self.info['vrf'][vrf]['address_family']['ipv6']['enable'] = True
                        break
            except:
                pass

            # delete unused ops attribute
            try:
                del(self.info['vrf'][vrf]['interface'])
            except:
                pass