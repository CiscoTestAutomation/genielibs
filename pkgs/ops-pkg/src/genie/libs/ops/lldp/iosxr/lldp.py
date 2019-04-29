''' 
LLDP Genie Ops Object for IOSXR - CLI.
'''
# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# Parser
from genie.libs.parser.iosxr.show_lldp import ShowLldp, \
                                   ShowLldpEntry, \
                                   ShowLldpNeighborsDetail,\
                                   ShowLldpTraffic, \
                                   ShowLldpInterface


class Lldp(Base):
    '''LLDP Genie Ops Object'''

    def tx_rx_both_enabled(self, item):
        '''return True when logic and for tx and rx is True'''
        if 'enabled' in item['tx'] and 'enabled' in item['rx']:
            return True
        else:
            return False
            
    def learn(self):
        '''Learn lldp Ops'''
        ########################################################################
        #                               info
        ########################################################################
        
        # unsupported keys
        # enabled
        # hello_timer
        # hold_timer
        # suppress_tlv_advertisement: - NA
        #   chassis_id - N/A
        #   port_id - N/A
        #   port_description - N/A
        #   system_name - N/A
        #   system_description - N/A
        #   system_capabilities - N/A
        #   management_address - N/A
        # system_name - N/A
        # system_description - N/A
        # chassis_id - N/A
        # chassis_id_type - N/A
        # counters
        #   frame_in
        #   frame_out
        #   frame_error_in
        #   frame_discard
        #   tlv_discard - N/A
        #   tlv_unknown - N/A
        #   last_clear - N/A
        #   tlv_accepted
        #   entries_aged_out
        # interfaces
        #     if_name
        #         if_name - N/A
        #         enabled
        #         counters - N/A
        #             frame_in - N/A
        #             frame_out - N/A
        #             frame_error_in - N/A
        #             frame_discard - N/A
        #             tlv_discard - N/A
        #             tlv_unknown - N/A
        #             last_clear - N/A
        #             frame_error_out - N/A
        #             entries_aged_out - N/A
        #         pord_id
        #             neighbors
        #                   neighbor_id
        #                       neighbor_id
        #                       system_name
        #                       system_description - N/A
        #                       chassis_id
        #                       chassis_id_type - N/A
        #                       id - N/A
        #                       age - N/A
        #                       last_update - N/A
        #                       port_id
        #                       port_id_type - N/A
        #                       port_description
        #                       management_address
        #                       management_address_type - N/A
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

        nbr_src = '[interfaces][(?P<intf>.*)][port_id][(?P<p_id>.*)][neighbors][(?P<nei>.*)]'
        nbr_dest = 'info[interfaces][(?P<intf>.*)][port_id][(?P<p_id>.*)][neighbors][(?P<nei>.*)]'

        for key in ['enabled', 'hello_timer', 'hold_timer']:
            self.add_leaf(cmd=ShowLldp,
                          src='[{}]'.format(key),
                          dest='info[{}]'.format(key))

        for key in ['[neighbor_id]', '[system_name]', '[system_description]', '[chassis_id]',
          '[port_id]', '[port_description]', '[management_address]',
           '[capabilities][(?P<cap>.*)][enabled]' ]:
            self.add_leaf(cmd=ShowLldpEntry,
                          src=nbr_src + key,
                          dest=nbr_dest + key)

        for key in ['[neighbor_id]', '[system_name]', '[system_description]', '[chassis_id]',
          '[port_id]', '[port_description]', '[management_address]',
          '[capabilities][(?P<cap>.*)][enabled]' ]:
            self.add_leaf(cmd=ShowLldpNeighborsDetail,
                          src=nbr_src + key,
                          dest=nbr_dest + key)

        for key in ['frame_in', 'frame_out', 'frame_error_in', 'frame_discard',
          'tlv_discard', 'tlv_unknown', 'entries_aged_out']:
            self.add_leaf(cmd=ShowLldpTraffic,
                          src='[counters][{}]'.format(key),
                          dest='info[counters][{}]'.format(key))

        intf_src = '[interfaces][(?P<intf>.*)]'
        intf_dest = 'info[interfaces][(?P<intf>.*)]'

        # enabled
        self.add_leaf(cmd=ShowLldpInterface,
                      src=intf_src,
                      dest=intf_dest + '[enabled]',
                      action=self.tx_rx_both_enabled)

        # make to write in cache
        self.make(final_call=True)
