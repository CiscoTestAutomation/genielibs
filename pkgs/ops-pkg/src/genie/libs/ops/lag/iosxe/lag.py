''' 
LAG Genie Ops Object for IOSXE - CLI.
'''
# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# Parser
from genie.libs.parser.iosxe.show_lag import ShowLacpSysId, \
                                             ShowLacpCounters, \
                                             ShowEtherchannelSummary,\
                                             ShowLacpNeighbor,\
                                             ShowPagpCounters, \
                                             ShowPagpNeighbor,\
                                             ShowPagpInternal


class Lag(Base):
    '''LAG Genie Ops Object'''

    def learn(self):
        '''Learn lag Ops'''
        
        ########################################################################
        #                               info
        ########################################################################
        # Keys not supported in iosxe
        # enabled, lacp_rx_errors, lacp_tx_errors, lacp_unknown_erros
        # interval, lacp_mode, lacp_max_bundle, lacp_min_bundle
        # force, non_silent, timeout, synchronization, aggregatable
        # collecting, distributing, system_id, partner_key, partner_port_num
        
        # system_priority
        self.add_leaf(cmd=ShowLacpSysId,
                      src='[system_priority]',
                      dest='info[system_priority]')

        # -----------   interfaces ------------
        intf_src = '[interfaces][(?P<intf>.*)]'
        intf_dst = 'info[interfaces][(?P<intf>.*)]'

        # name, bundle_id, protocol, oper_status
        for key in ['name', 'bundle_id', 'protocol', 'oper_status']:
            self.add_leaf(cmd=ShowEtherchannelSummary,
                          src=intf_src + '[{}]'.format(key),
                          dest=intf_dst + '[{}]'.format(key))

        # system_priority, system_id_mac
        for key in ['system_priority', 'system_id_mac']:
            self.add_leaf(cmd=ShowLacpSysId,
                          src='[{}]'.format(key),
                          dest=intf_dst + '[{}]'.format(key))

        # -----------   members ------------
        mem_src = intf_src + '[members][(?P<mem>.*)]'
        mem_dst = intf_dst + '[members][(?P<mem>.*)]'

        # bundled, interface
        for key in ['bundled', 'interface']:
            self.add_leaf(cmd=ShowEtherchannelSummary,
                          src=mem_src + '[{}]'.format(key),
                          dest=mem_dst + '[{}]'.format(key))

        # activity, partner_id, age
        for key in ['activity', 'partner_id', 'age']:
            for cmd in [ShowLacpNeighbor, ShowPagpNeighbor]:
                self.add_leaf(cmd=cmd,
                              src=mem_src + '[{}]'.format(key),
                              dest=mem_dst + '[{}]'.format(key))

        # oper_key, port_num, lacp_port_priority
        for key in ['oper_key', 'port_num', 'lacp_port_priority']:
            self.add_leaf(cmd=ShowLacpNeighbor,
                          src=mem_src + '[{}]'.format(key),
                          dest=mem_dst + '[{}]'.format(key))       

        # pagp_port_priority
        self.add_leaf(cmd=ShowPagpInternal,
                      src=mem_src + '[pagp_port_priority]',
                      dest=mem_dst + '[pagp_port_priority]')

        # -----------   counters ------------
        count_src = mem_src + '[counters]'
        count_dst = mem_dst + '[counters]'

        # lacp_in_pkts, lacp_out_pkts, lacp_errors
        for key in ['lacp_in_pkts', 'lacp_out_pkts', 'lacp_errors']:
            for cmd in [ShowLacpCounters, ShowPagpCounters]:
                self.add_leaf(cmd=cmd,
                              src=count_src + '[{}]'.format(key),
                              dest=count_dst + '[{}]'.format(key))

        # make to write in cache
        self.make(final_call=True)

        # bundle_id
        if hasattr(self, 'info'):
            for intf in self.info.get('interfaces', {}):
                bundle_id = self.info['interfaces'][intf].get('bundle_id', None)
                if not bundle_id:
                    continue
                for mem in self.info['interfaces'][intf].get('members', {}):
                    self.info['interfaces'][intf]['members'][mem]['bundle_id'] = bundle_id

