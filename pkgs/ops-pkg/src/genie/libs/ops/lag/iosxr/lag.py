''' 
LAG Genie Ops Object for IOSXR - CLI.
'''
# Genie
from genie.ops.base import Base
from genie.ops.base import Context

# Parser
from genie.libs.parser.iosxr.show_lag import ShowLacpSystemId, \
                                             ShowBundle, \
                                             ShowLacp

class Lag(Base):
    '''LAG Genie Ops Object'''

    def toInt(self, item):
        # 0x0001
        return int(item, 0)

    def getPortNum(self, item):
        # 0x8000,0x0002
        port_num = item.split(',')[1]
        return int(port_num, 0)

    def getPortPriority(self, item):
        # 0x8000,0x0002
        priority = item.split(',')[0]
        return int(priority, 0)

    def formatMAC(self, item):
        # 0x8000,00-0c-86-5e-68-23
        mac = item.split(',')[1].strip()
        mac = mac.replace('-', '').lower()
        mac = ".".join(["%s" % (mac[i:i+4]) for i in range(0, 12, 4)])
        return mac

    def getBundled(self, item):
        return True if item.lower() == 'active' else False

    def setProtocol(self, item):
        return 'lacp'

    def learn(self):
        '''Learn lag Ops'''
        
        ########################################################################
        #                               info
        ########################################################################
        # enabled                   N/A
        # system_priority 
        # interfaces 
        #     interface
        #         name
        #         interval                 N/A
        #         lacp_mode 
        #         lacp_max_bundle 
        #         lacp_min_bundle 
        #         system_id_mac 
        #         system_priority 
        #         bundle_id 
        #         protocol                
        #         oper_status
        #         members 
        #             member_interface 
        #                  bundle_id                 
        #                  bundled                   
        #                  interface
        #                  activity                  N/A
        #                  non_silent                N/A
        #                  force                     N/A
        #                  timeout                   N/A
        #                  synchronization
        #                  aggregatable
        #                  collecting
        #                  distributing
        #                  system_id 
        #                  oper_key
        #                  partner_id
        #                  partner_key
        #                  port_num
        #                  partner_port_num
        #                  lacp_port_priority        
        #                  pagp_port_priority        N/A
        #                  age                       N/A
        #                  counters                  N/A

        # ----------- system_priority ------------
        self.add_leaf(cmd=ShowLacpSystemId,
                      src='[system_priority]',
                      dest='info[system_priority]')

        # -----------   interfaces ------------
        intf_src = '[interfaces][(?P<intf>.*)]'
        intf_dst = 'info[interfaces][(?P<intf>.*)]'

        for key in ['name', 'bundle_id', 'oper_status']:
            self.add_leaf(cmd=ShowBundle,
                          src=intf_src + '[{}]'.format(key),
                          dest=intf_dst + '[{}]'.format(key))

        self.add_leaf(cmd=ShowBundle, 
                      src=intf_src + '[mac_address]',
                      dest=intf_dst + '[system_id_mac]')

        self.add_leaf(cmd=ShowBundle, 
                      src=intf_src + '[max_active_link]',
                      dest=intf_dst + '[lacp_max_bundle]')

        self.add_leaf(cmd=ShowBundle, 
                      src=intf_src + '[min_active_link]',
                      dest=intf_dst + '[lacp_min_bundle]')

        self.add_leaf(cmd=ShowLacp, 
                      src=intf_src + '[lacp_mode]',
                      dest=intf_dst + '[lacp_mode]')

        self.add_leaf(cmd=ShowLacp,
                      src=intf_src + '[lacp_mode]',
                      dest=intf_dst + '[protocol]',
                      action=self.setProtocol)
        self.make()
        
        # system_priority
        if hasattr(self, 'info') and 'system_priority' in self.info and 'interfaces' in self.info:
            system_priority = self.info['system_priority']
            for interface, intf_dict in self.info['interfaces'].items():
                intf_dict['system_priority'] = system_priority
                

        # -----------   members ------------
        mem_src = intf_src + '[port][(?P<mem>.*)]'
        mem_dst = intf_dst + '[members][(?P<mem>.*)]'

        for key in ['interface', 'synchronization', 'aggregatable', 'collecting', 'distributing', 'bundle_id']:
            self.add_leaf(cmd=ShowLacp,
                          src=mem_src + '[{}]'.format(key),
                          dest=mem_dst + '[{}]'.format(key))

        # bundled
        self.add_leaf(cmd=ShowBundle,
                      src=mem_src + '[state]',
                      dest=mem_dst + '[bundled]',
                      action=self.getBundled)

        self.add_leaf(cmd=ShowLacp,
                      src=mem_src + '[system_id]',
                      dest=mem_dst + '[system_id]',
                      action=self.formatMAC)

        self.add_leaf(cmd=ShowLacp,
                      src=mem_src + '[key]',
                      dest=mem_dst + '[oper_key]',
                      action=self.toInt)

        self.add_leaf(cmd=ShowLacp,
                      src=mem_src + '[port_id]',
                      dest=mem_dst + '[port_num]',
                      action=self.getPortNum)

        self.add_leaf(cmd=ShowLacp,
                      src=mem_src + '[port_id]',
                      dest=mem_dst + '[lacp_port_priority]',
                      action=self.getPortPriority)

        # -----------  partner  ------------
        partner_src = mem_src + '[partner]'
        self.add_leaf(cmd=ShowLacp,
                      src=partner_src + '[system_id]',
                      dest=mem_dst + '[partner_id]',
                      action=self.formatMAC)

        self.add_leaf(cmd=ShowLacp,
                      src=partner_src + '[key]',
                      dest=mem_dst + '[partner_key]',
                      action=self.toInt)

        self.add_leaf(cmd=ShowLacp,
                      src=partner_src + '[port_id]',
                      dest=mem_dst + '[partner_port_num]',
                      action=self.getPortNum)  

        # make to write in cache
        self.make(final_call=True)
        
