''' 
Platform Genie Ops Object for IOSXR.
'''

# super class
from genie.libs.ops.platform.platform import Platform as SuperPlatform

# Parser
from genie.libs.parser.iosxr.show_platform import ShowVersion, ShowSdrDetail,\
                                ShowPlatform, ShowPlatformVm,\
                                ShowInstallActiveSummary, ShowInventory,\
                                ShowRedundancySummary, AdminShowDiagChassis,\
                                ShowRedundancy, Dir


class Platform(SuperPlatform):
    '''Platform Genie Ops Object'''

    def get_active_uptime(self, item):
        for node in item:
            if 'active' in item[node]['role'].lower():
                return item[node]['node_uptime_in_seconds']
            
    def learn(self):
        '''Learn Platform Ops'''

        # ================
        # DeviceAttributes
        # ================

        # chassis
        self.add_leaf(cmd=ShowVersion,
                      src='[chassis_detail]',
                      dest='[chassis]')

        # chassis_sn
        self.add_leaf(cmd=AdminShowDiagChassis,
                      src='[sn]',
                      dest='[chassis_sn]')


        # rtr_type
        self.add_leaf(cmd=ShowVersion,
                      src='[device_family]',
                      dest='[rtr_type]')

        # os
        self.add_leaf(cmd=ShowVersion,
                      src='[operating_system]',
                      dest='[os]')

        # version
        self.add_leaf(cmd=ShowVersion,
                      src='[software_version]',
                      dest='[version]')

        # image
        self.add_leaf(cmd=ShowVersion,
                      src='[image]',
                      dest='[image]')

        # installed_packages
        self.add_leaf(cmd=ShowInstallActiveSummary,
                      src='[active_packages]',
                      dest='[installed_packages]')

        # config_register
        self.add_leaf(cmd=ShowVersion,
                      src='[config_register]',
                      dest='[config_register]')

        # main_mem
        self.add_leaf(cmd=ShowVersion,
                      src='[processor_memory_bytes]',
                      dest='[main_mem]')

        # dir
        self.add_leaf(cmd=Dir,
                      src='[dir]',
                      dest='[dir]')

        # sdr_owner
        self.add_leaf(cmd=ShowInstallActiveSummary,
                      src='[sdr]',
                      dest='[sdr_owner]')
        
        # =======================
        # VirtualDeviceAttributes
        # =======================

        # vd_id == sdr_id
        # vd_name == sdr_name
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][sdr_name][(?P<sdr_name>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_name][(?P<sdr_name>.*)]')

        # vd_dSDRsc_nod
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][dsdrsc_node][(?P<dsdrsc_node>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_dSDRsc_nod][(?P<dsdrsc_node>.*)]')

        # vd_dSDRsc_partner_node
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][dsdrsc_partner_node][(?P<dsdrsc_partner_node>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_dSDRsc_partner_node][(?P<dsdrsc_partner_node>.*)]')

        # vd_primary_node1
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][primary_node1][(?P<primary_node1>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_primary_node1][(?P<primary_node1>.*)]')

        # vd_primary_node2
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][primary_node2][(?P<primary_node2>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_primary_node2][(?P<primary_node2>.*)]')

        # vd_mac_addr
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][mac_address][(?P<mac_address>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_mac_addr][(?P<mac_address>.*)]')

        # ====================
        # MembershipAttributes
        # ====================

        # vd_ms_name == node_name
        # vd_ms_type == type
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][type][(?P<type>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][vd_ms_type][(?P<type>.*)]')

        # vd_ms_status
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][node_status][(?P<node_status>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][vd_ms_status][(?P<node_status>.*)]')

        # vd_ms_red_state
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][red_state][(?P<red_state>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][vd_ms_red_state][(?P<red_state>.*)]')

        # vd_ms_partner_name
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][partner_name][(?P<partner_name>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][vd_ms_partner_name][(?P<partner_name>.*)]')

        # ==============
        # SlotAttributes
        # ==============

        # card_name
        self.add_leaf(cmd=ShowPlatform,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][name][(?P<card_name>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][name][(?P<card_name>.*)]')

        # state
        self.add_leaf(cmd=ShowPlatform,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][state][(?P<state>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][state][(?P<state>.*)]')

        # config_state
        self.add_leaf(cmd=ShowPlatform,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][config_state][(?P<config_state>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][config_state][(?P<config_state>.*)]')

        # redundancy_state
        self.add_leaf(cmd=ShowPlatform,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][redundancy_state][(?P<redundancy_state>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][redundancy_state][(?P<redundancy_state>.*)]')

        # subslot
        self.add_leaf(cmd=ShowPlatform,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][subslot][(?P<subslot>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][subslot][(?P<subslot>.*)]')

        # rp_config_register
        self.add_leaf(cmd=ShowVersion,
                      src='[rp_config_register][(?P<rp_config_register>.*)]',
                      dest='[slot][rp][rp_config_register][(?P<rp_config_register>.*)]')

        # ==============
        # Redudancy
        # ==============

        # redundancy_communication
        self.add_leaf(cmd=ShowRedundancySummary,
                      src='[redundancy_communication]',
                      dest='[redundancy_communication]')

        # rp_uptime
        self.add_leaf(cmd=ShowRedundancy,
                      src='[node]',
                      dest='[rp_uptime]',
                      action=self.get_active_uptime)

        # Make Ops object
        self.make(final_call=True)

# vim: ft=python et sw=4
