''' 
LLDP Genie Ops Object for IOSXE - CLI.
'''
# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# Parser
from genie.libs.parser.iosxe.show_lldp import ShowLldp, ShowLldpNeighborsDetail,\
                                   ShowLldpTraffic, \
                                   ShowLldpInterface


class Lldp(Base):
    '''LLDP Genie Ops Object'''

    def tx_rx_both_enabled(self, item):
        '''return True when logic and for tx and rx is True'''
        try:
            if 'enabled' in item['tx'] and 'enabled' in item['rx']:
                return True
            else:
                return False
        except Exception:
            return False

    def learn(self):
        '''Learn Spanning-tree Ops'''
        
        ########################################################################
        #                               info
        ########################################################################
        
        for key in ['enabled', 'hello_timer', 'hold_timer']:
            self.add_leaf(cmd=ShowLldp,
                          src='[{}]'.format(key),
                          dest='info[{}]'.format(key))

        # suppress_tlv_advertisement, system_name are not supported
        # system_description, chassis_id, chassis_id_type are not supported

        # counters
        # last_clear and tlv_accepted are not supported
        for key in ['frame_in', 'frame_out', 'frame_error_in', 'frame_discard',
          'tlv_discard', 'tlv_unknown', 'entries_aged_out']:
            self.add_leaf(cmd=ShowLldpTraffic,
                          src='[{}]'.format(key),
                          dest='info[counters][{}]'.format(key))

        # interface neighbors attribtues
        # Unsupported Attributes - id, age, last_update, chassis_id_type
        #                          port_id_type, management_address_type,
        #                          custom_tlvs, counters

        intf_src = '[interfaces][(?P<intf>.*)]'
        intf_dest = 'info[interfaces][(?P<intf>.*)]'

        nbr_src = '[interfaces][(?P<intf>.*)][neighbors][(?P<nei>.*)]'
        nbr_dest = 'info[interfaces][(?P<intf>.*)][neighbors][(?P<nei>.*)]'

        self.add_leaf(cmd=ShowLldpNeighborsDetail,
                      src=intf_src + '[if_name]',
                      dest=intf_dest + '[if_name]')

        for key in ['[chassis_id]', '[port_id]', '[neighbor_id]', '[system_name]',
          '[system_description]', '[port_description]', '[management_address]',
          '[capabilities][(?P<cap>.*)][enabled]','[capabilities][(?P<cap>.*)][name]' ]:
            self.add_leaf(cmd=ShowLldpNeighborsDetail,
                          src=nbr_src + key,
                          dest=nbr_dest + key)
        # enabled
        self.add_leaf(cmd=ShowLldpInterface,
                      src=intf_src,
                      dest=intf_dest + '[enabled]',
                      action=self.tx_rx_both_enabled)

        # make to write in cache
        self.make()
