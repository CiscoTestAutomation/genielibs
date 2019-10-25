# Genie package
from genie.libs.ops.vlan.vlan import Vlan as SuperVlan

# genie.libs
from genie.libs.parser.iosxr import show_ethernet


class Vlan(SuperVlan):
    '''Vlan Ops Object'''

    def learn(self):
        '''Learn Vlan object'''

        # Place holder to make it more readable
        src_ethernet_tag = '[interface][(?P<interface>.*)][sub_interface]\
                            [(?P<sub_interface>.*)][vlan_id][(?P<vlan_id>.*)]'
        dest_ethernet_tag = 'name[(?P<vlan_id>.*)]'

        self.add_leaf(cmd=show_ethernet.ShowEthernetTags,
                      src=src_ethernet_tag,
                      dest='name[(?P<vlan_id>.*)]\
                            [sub_interface][(?P<sub_interface>.*)]')

        self.add_leaf(cmd=show_ethernet.ShowEthernetTags,
                      src=src_ethernet_tag+'[outer_encapsulation_type]',
                      dest=dest_ethernet_tag+'[ethernet_encapsulation_type]')

        self.add_leaf(cmd=show_ethernet.ShowEthernetTags,
                      src=src_ethernet_tag+'[inner_encapsulation_type]',
                      dest=dest_ethernet_tag+'[inner_encapsulation_type]')

        self.add_leaf(cmd=show_ethernet.ShowEthernetTags,
                      src=src_ethernet_tag+'[inner_encapsulation_vlan_id]',
                      dest=dest_ethernet_tag+'[inner_encapsulation_vlan_id]')

        self.make(final_call=True)
        # Handling the case of having many sub_interfaces under one interface
        # so showing them as a list under the main interface.
        if hasattr(self, 'name'):
            for vlan in self.name.keys():
                sub_interfaces = []
                if 'sub_interface' in self.name[vlan]:
                    for sub_interface in self.name[vlan]['sub_interface'].keys():
                        sub_interfaces.append(sub_interface)
                    sub_interfaces = ', '.join(sub_interfaces)
                    self.name[vlan]['sub_interface'] = sub_interfaces
