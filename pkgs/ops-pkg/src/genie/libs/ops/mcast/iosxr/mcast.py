''' 
MCAST Genie Ops Object for IOSXR - CLI.
'''
# super class
from genie.libs.ops.mcast.mcast import Mcast as SuperMacst

# nxos show_mcast
from genie.libs.parser.iosxr.show_pim import ShowPimVrfMstatic, ShowPimVrfRpfSummary,\
                                  ShowPimVrfInterfaceDetail

# iosxr show_mrib
from genie.libs.parser.iosxr.show_mrib import ShowMribVrfRoute

# iosxr show_vrf
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail

class Mcast(SuperMacst):
    '''Mcast Genie Ops Object'''

    def set_enable(self, item):
        try:
            item.keys()
            return True
        except:
            return False

    def learn(self):
        '''Learn Mcast Ops'''

        # vrf
        #   vrf_name
        #     address_family
        #       af_name
        info_src = '[vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)]'
        info_dest = 'info' + info_src

        # vrf
        #   vrf_name
        #     address_family
        #       af_name
        #         multicast_group
        #           group_name
        #             source_address
        #               address_name
        tbl_src = '[vrf][(?P<vrf>.*)][address_family][(?P<address_family>.*)][multicast_group][(?P<multicast_group>.*)][source_address][(?P<source_address>.*)]'
        tbl_dest = 'table' + tbl_src

        # Get list of vrfs present on system
        self.add_leaf(cmd=ShowVrfAllDetail,
                     src='',
                     dest='list_of_vrfs',
                     action=lambda x: list(x.keys()))
        self.make()

        if hasattr(self, 'list_of_vrfs'):

            for vrf in sorted(self.list_of_vrfs):
                
                for af in ['ipv4', 'ipv6']:

                    ############################################################
                    #                           INFO
                    ############################################################

                    # enable
                    self.add_leaf(cmd=ShowPimVrfInterfaceDetail,
                                  src='[vrf][(?P<vrf>.*)][interfaces]',
                                  dest='info[vrf][(?P<vrf>.*)][address_family][{af}][enable]'.format(af=af),
                                  vrf=vrf, af=af,
                                  action=self.set_enable)

                    # multipath
                    self.add_leaf(cmd=ShowPimVrfRpfSummary,
                                  src=info_src+'[multipath]',
                                  dest=info_dest+'[multipath]',
                                  vrf=vrf, af=af)

                    # mroute
                    self.add_leaf(cmd=ShowPimVrfMstatic,
                                  src=info_src+'[mroute]',
                                  dest=info_dest+'[mroute]',
                                  vrf=vrf, af=af)

                    ############################################################
                    #                           TABLE
                    ############################################################

                    # flags
                    self.add_leaf(cmd=ShowMribVrfRoute,
                                  src=tbl_src+'[flags]',
                                  dest=tbl_dest+'[flags]',
                                  vrf=vrf, af=af)

                    # uptime
                    self.add_leaf(cmd=ShowMribVrfRoute,
                                  src=tbl_src+'[uptime]',
                                  dest=tbl_dest+'[uptime]',
                                  vrf=vrf, af=af)

                    # incoming_interface_list
                    #   rpf_nbr
                    self.add_leaf(cmd=ShowMribVrfRoute,
                                  src=tbl_src+'[incoming_interface_list][(?P<intf>.*)][rpf_nbr]',
                                  dest=tbl_dest+'[incoming_interface_list][(?P<intf>.*)][rpf_nbr]',
                                  vrf=vrf, af=af)

                    # outgoing_interface_list
                    #   uptime
                    self.add_leaf(cmd=ShowMribVrfRoute,
                                  src=tbl_src+'[outgoing_interface_list][(?P<intf>.*)][uptime]',
                                  dest=tbl_dest+'[outgoing_interface_list][(?P<intf>.*)][uptime]',
                                  vrf=vrf, af=af)

                    # outgoing_interface_list
                    #   flags
                    self.add_leaf(cmd=ShowMribVrfRoute,
                                  src=tbl_src+'[outgoing_interface_list][(?P<intf>.*)][flags]',
                                  dest=tbl_dest+'[outgoing_interface_list][(?P<intf>.*)][flags]',
                                  vrf=vrf, af=af)

        # Make final Ops structure
        self.make(final_call=True)