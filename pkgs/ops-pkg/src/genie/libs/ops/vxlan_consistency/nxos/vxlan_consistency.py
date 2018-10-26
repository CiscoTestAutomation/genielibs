# Genie package
from genie.ops.base import Base

# genie.libs
from genie.libs.parser.nxos.show_interface import ShowRunningConfigInterface,\
                                                  ShowNveInterface
from genie.libs.parser.nxos.show_fdb import ShowMacAddressTableVni
from genie.libs.parser.nxos.show_l2route import ShowL2routeEvpnMacEvi
from genie.libs.parser.nxos.show_bgp import ShowBgpL2vpnEvpnWord


class VxlanConsistency(Base):
    '''VxlanConsistency Ops Object'''

    def learn(self, intf):
        '''Learn VxlanConsistency object'''

        self.add_leaf(cmd=ShowRunningConfigInterface,
                      src='[interface][(?P<interface>.*)][member_vni]\
                            [(?P<member_vni>.*)]',
                      dest='info[interface][(?P<interface>.*)][member_vni][(?P<member_vni>.*)]',
                      intf=intf)

        self.make()

        # Only one interface is found under info['interface']
        if hasattr(self, 'info') and 'interface' in self.info:
            interface = next(iter(self.info['interface'].keys()))
        else:
            return

        if 'member_vni' in self.info['interface'][interface]:

            for vni in sorted(self.info['interface'][interface]['member_vni']):

                destination = 'info[interface][{l}][member_vni][{k}]'.format(l=interface,k=vni)

                # Remote - next_hop
                self.add_leaf(cmd=ShowMacAddressTableVni,
                              src='[mac_address][(?P<mac_address>.*)][next_hop]',
                              dest=destination+'[remote][mac_address][(?P<mac_address>.*)][next_hop]',
                              vni=vni,
                              intf=interface)

                # Remote - evi
                self.add_leaf(cmd=ShowMacAddressTableVni,
                              src='[mac_address][(?P<mac_address>.*)][evi]',
                              dest=destination+'[remote][mac_address][(?P<mac_address>.*)][evi]',
                              vni=vni,
                              intf=interface)

                # Local - next_hop
                self.add_leaf(cmd=ShowMacAddressTableVni,
                              src='[mac_address][(?P<mac_address>.*)][ports]',
                              dest=destination+'[local][mac_address][(?P<mac_address>.*)][next_hop]',
                              vni=vni)

                # Local - evi
                self.add_leaf(cmd=ShowMacAddressTableVni,
                              src='[mac_address][(?P<mac_address>.*)][evi]',
                              dest=destination+'[local][mac_address][(?P<mac_address>.*)][evi]',
                              vni=vni)

                self.make()

                for mac in sorted(self.info['interface'][interface]['member_vni'][vni].get('remote', {}).get('mac_address', [])):

                    evi = self.info['interface'][interface]['member_vni'][vni]['remote']['mac_address'][mac]['evi']

                    # Remote - next_hop
                    self.add_leaf(cmd=ShowL2routeEvpnMacEvi,
                                  src='[topology][(?P<topology>.*)][mac_address][(?P<mac_address>.*)][next_hops]',
                                  dest=destination+'[remote][mac_address][(?P<mac_address>.*)][topology][(?P<topology>.*)][next_hop]',
                                  evi=evi,
                                  mac=mac)

                    # Remote - prod
                    self.add_leaf(cmd=ShowL2routeEvpnMacEvi,
                                  src='[topology][(?P<topology>.*)][mac_address][(?P<mac_address>.*)][prod]',
                                  dest=destination+'[remote][mac_address][(?P<mac_address>.*)][topology][(?P<topology>.*)][prod]',
                                  evi=evi,
                                  mac=mac)

                    # Remote - next_hop
                    self.add_leaf(cmd=ShowBgpL2vpnEvpnWord,
                                  src='[mac_address][(?P<mac_address>.*)][next_hop]',
                                  dest=destination+'[remote][verified_structure][mac_address][(?P<mac_address>.*)][next_hop]',
                                  mac=mac,
                                  count1='10')

                    # Remote - received_label
                    self.add_leaf(cmd=ShowBgpL2vpnEvpnWord,
                                  src='[mac_address][(?P<mac_address>.*)][received_label]',
                                  dest=destination+'[remote][verified_structure][mac_address][(?P<mac_address>.*)][received_label]',
                                  mac=mac,
                                  count1='10')

                    self.make()

                for mac in sorted(self.info['interface'][interface]['member_vni'][vni].get('local', {}).get('mac_address', [])):

                    evi = self.info['interface'][interface]['member_vni'][vni]['local']['mac_address'][mac]['evi']

                    # local - next_hop
                    self.add_leaf(cmd=ShowL2routeEvpnMacEvi,
                                  src='[topology][(?P<topology>.*)][mac_address][(?P<mac_address>.*)][next_hops]',
                                  dest=destination+'[local][mac_address][(?P<mac_address>.*)][topology][(?P<topology>.*)][next_hop]',
                                  evi=evi,
                                  mac=mac)

                    # local - prod
                    self.add_leaf(cmd=ShowL2routeEvpnMacEvi,
                                  src='[topology][(?P<topology>.*)][mac_address][(?P<mac_address>.*)][prod]',
                                  dest=destination+'[local][mac_address][(?P<mac_address>.*)][topology][(?P<topology>.*)][prod]',
                                  evi=evi,
                                  mac=mac)

                    # local - primary
                    self.add_leaf(cmd=ShowNveInterface,
                                  src='[interface][(?P<interface>.*)][source_interface][(?P<source_interface>.*)][primary]',
                                  dest=destination+'[local][verified_structure][source_interface][(?P<source_interface>.*)][primary]',
                                  intf=interface)

                    # local - secondary
                    self.add_leaf(cmd=ShowNveInterface,
                                  src='[interface][(?P<interface>.*)][source_interface][(?P<source_interface>.*)][secondary]',
                                  dest=destination+'[local][verified_structure][source_interface][(?P<source_interface>.*)][secondary]',
                                  intf=interface)

                    # local - notified
                    self.add_leaf(cmd=ShowNveInterface,
                                  src='[interface][(?P<interface>.*)][vpc_capability][(?P<vpc_capability>.*)][notified]',
                                  dest=destination+'[local][verified_structure][vpc_capability][(?P<vpc_capability>.*)][notified]',
                                  intf=interface)

                    # local - next_hop
                    self.add_leaf(cmd=ShowBgpL2vpnEvpnWord,
                                  src='[mac_address][(?P<mac_address>.*)][next_hop]',
                                  dest=destination+'[local][verified_structure][mac_address][(?P<mac_address>.*)][next_hop]',
                                  mac=mac,
                                  count1='8',
                                  count2='10')

                    # local - received_label
                    self.add_leaf(cmd=ShowBgpL2vpnEvpnWord,
                                  src='[mac_address][(?P<mac_address>.*)][received_label]',
                                  dest=destination+'[local][verified_structure][mac_address][(?P<mac_address>.*)][received_label]',
                                  mac=mac,
                                  count1='8',
                                  count2='10')

                    self.make()