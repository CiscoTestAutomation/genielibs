'''
LLDP Genie Ops Object for NXOS - CLI.
'''
import re
# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# Parser
from genie.libs.parser.nxos.show_lldp import ShowLldpAll, ShowLldpTimers, \
    ShowLldpTlvSelect, ShowLldpNeighborsDetail, ShowLldpTraffic


class Lldp(Base):
    """LLDP Genie Ops Object"""

    def learn(self):
        """Learn lldp Ops"""
        ########################################################################
        #                               info
        ########################################################################

        # enabled -N/A
        # hello_timer
        # hold_timer
        # suppress_tlv_advertisement:
        #   chassis_id -NA
        #   port_id -N/A
        #   port_description
        #   system_name
        #   system_description
        #   system_capabilities
        #   management_address
        # system_name -N/A
        # system_description -N/A
        # chassis_id -N/A
        # chassis_id_type -N/A
        # counters
        #   frame_in
        #   frame_out
        #   frame_error_in
        #   frame_discard
        #   tlv_discard - N/A
        #   tlv_unknown
        #   last_clear - N/A
        #   tlv_accepted - N/A
        #   entries_aged_out
        # interfaces
        #     if_name
        #         if_name
        #         enabled
        #         counters - N/A
        #             frame_in - N/A
        #             frame_out - N/A
        #             frame_error_in - N/A
        #             frame_discard - N/A
        #             tlv_discard -N/A
        #             tlv_unknown - N/A
        #             last_clear - N/A
        #             frame_error_out - N/A
        #             entries_aged_out - N/A
        #         pord_id
        #             neighbors
        #                   neighbor_id
        #                       neighbor_id - N/A
        #                       system_name
        #                       system_description
        #                       chassis_id
        #                       chassis_id_type - N/A
        #                       id -N/A
        #                       age -N/A
        #                       last_update -N/A
        #                       port_id
        #                       port_id_type - N/A
        #                       port_description
        #                       management_address
        #                       management_address_v6
        #                       management_address_type
        #                       custom_tlvs' - N/A
        #                           [type oui oui_subtype] - N/A
        #                               type - N/A
        #                               oui - N/A
        #                               oui_subtype - N/A
        #                               value - N/A
        #                       capabilities
        #                           name
        #                               name
        #                               enabled
        #                               system

        for key in ['hello_timer', 'hold_timer']:
            self.add_leaf(cmd=ShowLldpTimers, src='[{}]'.format(key),
                          dest='info[{}]'.format(key))
        for key in ['port_description', 'system_name',
                    'system_description', 'system_capabilities']:
            self.add_leaf(cmd=ShowLldpTlvSelect,
                          src='suppress_tlv_advertisement[{}]'.format(key),
                          dest='info[suppress_tlv_advertisement][{}]'.format(key))

        self.add_leaf(cmd=ShowLldpTlvSelect,
                      src='suppress_tlv_advertisement[management_address_v4]',
                      dest='info[suppress_tlv_advertisement][management_address]')

        ops_counter_keys = ['frame_in', 'frame_out', 'frame_error_in', 'frame_discard',
                            'tlv_unknown', 'entries_aged_out']
        parser_counter_list=['total_frames_received', 'total_frames_transmitted',
                           'total_frames_received_in_error',
                           'total_frames_discarded', 'total_unrecognized_tlvs',
                           'total_entries_aged']
        for key in parser_counter_list:
            self.add_leaf(cmd=ShowLldpTraffic,
                          src='counters[{}]'.format(key),
                          dest='info[counters][{}]'.format(ops_counter_keys[parser_counter_list.index(key)]))

        nbr_src = '[interfaces][(?P<intf>.*)][port_id][(?P<p_id>.*)][neighbors][(' \
                  '?P<nei>.*)]'
        nbr_dest = 'info[interfaces][(?P<intf>.*)][port_id][(?P<p_id>.*)][neighbors][(' \
                   '?P<nei>.*)]'

        for key in ['[chassis_id]', '[port_id]', '[system_name]',
                    '[system_description]', '[port_description]',
                    '[capabilities][(?P<cap>.*)][enabled]', '[capabilities][(?P<cap>.*)][system]',
                    '[capabilities][(?P<cap>.*)][name]']:
            self.add_leaf(cmd=ShowLldpNeighborsDetail,
                          src=nbr_src + key,
                          dest=nbr_dest + key)
        # mgmt_address v4
        self.add_leaf(cmd=ShowLldpNeighborsDetail,
                      src='[interfaces][(?P<intf>.*)][port_id][(?P<p_id>.*)][neighbors][(' \
                  '?P<nei>.*)][management_address_v4]',
                      dest='info[interfaces][(?P<intf>.*)][port_id][(?P<p_id>.*)][neighbors][(' \
                   '?P<nei>.*)][management_address]')
        # mgmt_address v6
        self.add_leaf(cmd=ShowLldpNeighborsDetail,
                      src='[interfaces][(?P<intf>.*)][port_id][(?P<p_id>.*)][neighbors][(' \
                  '?P<nei>.*)][management_address_v6]',
                      dest='info[interfaces][(?P<intf>.*)][port_id][(?P<p_id>.*)][neighbors][(' \
                   '?P<nei>.*)][management_address_v6]')
        self.add_leaf(cmd=ShowLldpAll,
                      src='interfaces[(?P<intf>.*)][enabled]',
                      dest='info[interfaces][(?P<intf>.*)][enabled]')
        # cache result
        self.make()
        if hasattr(self, 'info') and 'interfaces' in self.info:
            for intf in self.info['interfaces']:
                if 'port_id' in self.info['interfaces'][intf]:
                    for port_id in self.info['interfaces'][intf]['port_id']:
                        for neighbors in self.info['interfaces'][intf]['port_id'][port_id]['neighbors']:
                            # if ipv6 is empty set type = ipv4
                            if self.info['interfaces'][intf]['port_id'][port_id]['neighbors'][neighbors].get('management_address_v6') == 'not advertised':
                                self.info['interfaces'][intf]['port_id'][port_id][
                                    'neighbors'][neighbors]['management_address_type'] = 'ipv4'
                                del self.info['interfaces'][intf]['port_id'][port_id]['neighbors'][neighbors]['management_address_v6']
                            # if ipv4 is empty set type == ipv6
                            elif self.info['interfaces'][intf]['port_id'][port_id]['neighbors'][neighbors]['management_address'] == 'not advertised':
                                self.info['interfaces'][intf]['port_id'][port_id][
                                    'neighbors'][neighbors]['management_address_type'] = 'ipv6'
                                del self.info['interfaces'][intf]['port_id'][port_id]['neighbors'][neighbors]['management_address_v4']
                            else:
                                self.info['interfaces'][intf]['port_id'][port_id][
                                    'neighbors'][neighbors][
                                    'management_address_type'] = 'both'


        # if_name
        if hasattr(self, 'info') and 'interfaces' in self.info:
            for intf in self.info['interfaces']:
                self.info['interfaces'][intf]['if_name'] = intf
        # port_id
        if hasattr(self, 'info') and 'interfaces' in self.info:
            for intf in self.info['interfaces']:
                if 'port_id' in self.info['interfaces'][intf]:
                    for port_id in self.info['interfaces'][intf]['port_id']:
                        for neighbors in self.info['interfaces'][intf]['port_id'][port_id]['neighbors']:
                            self.info['interfaces'][intf]['port_id'][port_id]['neighbors'][neighbors]['port_id']=port_id

        self.make(final_call=True)


